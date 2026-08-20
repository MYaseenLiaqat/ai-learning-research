/* Participant-facing study application.
 * The backend is authoritative for task availability, timers, AI eligibility,
 * interaction cap, submissions, and scheduling. The frontend only renders
 * what the backend returns and never independently unlocks phases.
 */
(function () {
  "use strict";

  var API = ""; // same origin; adjust if frontend is served separately
  var STORAGE_KEY = "study_participant_id";

  var state = {
    learnerId: null,
    learner: null,
    tasks: [],
    currentTask: null,
    timerHandle: null,
  };

  // ---- DOM refs ----
  var $ = function (id) {
    return document.getElementById(id);
  };
  var screens = {
    entry: $("screen-entry"),
    home: $("screen-home"),
    task: $("screen-task"),
    complete: $("screen-complete"),
  };

  // ---- Helpers ----
  function showScreen(name) {
    Object.keys(screens).forEach(function (k) {
      screens[k].hidden = k !== name;
    });
  }

  function showError(el, msg) {
    el.textContent = msg;
    el.hidden = false;
  }

  function clearError(el) {
    el.hidden = true;
    el.textContent = "";
  }

  function api(path, options) {
    options = options || {};
    options.headers = options.headers || {};
    options.headers["Content-Type"] = "application/json";
    return fetch(API + path, options).then(function (resp) {
      return resp.json().then(function (data) {
        if (!resp.ok) {
          var err = new Error(
            (data && data.detail) || "Request failed: " + resp.status,
          );
          err.status = resp.status;
          throw err;
        }
        return data;
      });
    });
  }

  function get(path) {
    return api(path);
  }
  function post(path, body) {
    return api(path, { method: "POST", body: JSON.stringify(body || {}) });
  }

  function saveLearnerId(id) {
    try {
      localStorage.setItem(STORAGE_KEY, String(id));
    } catch (e) {
      /* ignore */
    }
  }
  function loadLearnerId() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function taskLabel(type) {
    switch (type) {
      case "supported":
        return "Learning task";
      case "immediate":
        return "Assessment 1";
      case "delayed":
        return "Assessment 2";
      case "transfer":
        return "Assessment 3";
      case "criterion":
        return "Assessment 4";
      default:
        return "Task";
    }
  }

  function formatDate(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    return d.toLocaleString();
  }

  // ---- Identity ----
  function ensureLearner(code) {
    // If code is numeric, try to load existing learner; else create new.
    var numeric = /^\d+$/.test(code);
    if (numeric) {
      return get("/learners/" + code)
        .then(function (learner) {
          return learner;
        })
        .catch(function (err) {
          if (err.status === 404) {
            return createLearner();
          }
          throw err;
        });
    }
    return createLearner();
  }

  function createLearner() {
    return post("/learners", { prior_ability_score: null }).then(
      function (learner) {
        return learner;
      },
    );
  }

  // ---- Task loading ----
  function loadTasks() {
    return get("/tasks/learner/" + state.learnerId).then(function (tasks) {
      state.tasks = tasks;
      return tasks;
    });
  }

  function loadStatus() {
    return get("/learners/" + state.learnerId + "/status");
  }

  // ---- Rendering: home ----
  function renderHome() {
    var list = $("task-list");
    list.innerHTML = "";
    var msg = $("home-message");
    msg.textContent = "";

    if (state.tasks.length === 0) {
      // No currently available tasks. Determine completion vs return-later.
      loadStatus()
        .then(function (status) {
          if (status.has_future_assessments) {
            msg.textContent =
              "You have completed the current part. Please return later for the next assessment.";
          } else {
            msg.textContent = "You have completed the study. Thank you!";
          }
        })
        .catch(function () {
          msg.textContent = "No tasks are currently available.";
        });
      return;
    }

    state.tasks.forEach(function (t) {
      var card = document.createElement("div");
      card.className = "task-card";

      var title = document.createElement("h3");
      title.textContent = taskLabel(t.type);
      card.appendChild(title);

      var p = document.createElement("p");
      p.textContent = t.prompt_text;
      card.appendChild(p);

      var btn = document.createElement("button");
      btn.textContent = "Start";
      btn.addEventListener("click", function () {
        openTask(t);
      });
      card.appendChild(btn);

      list.appendChild(card);
    });
  }

  // ---- Rendering: task ----
  function openTask(task) {
    state.currentTask = task;
    $("task-title").textContent = taskLabel(task.type);
    $("task-prompt").textContent = task.prompt_text;
    $("code-input").value = "";
    $("submit-status").hidden = true;
    $("submit-btn").disabled = false;

    // Timer: only for Supported, and only if started.
    var timerEl = $("task-timer");
    if (task.type === "supported" && task.started_at) {
      timerEl.hidden = false;
      startTimer(task.expires_at);
    } else {
      timerEl.hidden = true;
      stopTimer();
    }

    // AI panel: only for Supported AND AI condition.
    var aiPanel = $("ai-panel");
    var isAiCondition =
      state.learner && state.learner.condition === "controlled_ai";
    if (task.type === "supported" && isAiCondition) {
      aiPanel.hidden = false;
      $("ai-chat").innerHTML = "";
      $("ai-input").value = "";
      $("ai-status").hidden = true;
      updateAiRemaining(task.remaining_interactions);
    } else {
      aiPanel.hidden = true;
    }

    showScreen("task");
  }

  function startTimer(expiresIso) {
    stopTimer();
    var timerEl = $("task-timer");
    function tick() {
      var now = Date.now();
      var expires = new Date(expiresIso).getTime();
      var diff = expires - now;
      if (diff <= 0) {
        timerEl.textContent = "Time expired";
        timerEl.classList.add("expired");
        $("submit-btn").disabled = true;
        stopTimer();
        return;
      }
      var mins = Math.floor(diff / 60000);
      var secs = Math.floor((diff % 60000) / 1000);
      timerEl.textContent =
        "Time remaining: " + mins + ":" + (secs < 10 ? "0" : "") + secs;
      timerEl.classList.remove("expired");
    }
    tick();
    state.timerHandle = setInterval(tick, 1000);
  }

  function stopTimer() {
    if (state.timerHandle) {
      clearInterval(state.timerHandle);
      state.timerHandle = null;
    }
  }

  function updateAiRemaining(remaining) {
    $("ai-remaining").textContent =
      "AI interactions remaining: " + remaining + " of 8";
  }

  // ---- Submission ----
  function submitCurrent() {
    var task = state.currentTask;
    var code = $("code-input").value;
    var statusEl = $("submit-status");
    statusEl.hidden = false;
    statusEl.className = "status";
    statusEl.textContent = "Submitting...";
    $("submit-btn").disabled = true;

    post("/tasks/" + task.id + "/submit?learner_id=" + state.learnerId, {
      code: code,
    })
      .then(function (result) {
        statusEl.className = "status ok";
        statusEl.textContent = result.passed
          ? "Submitted successfully."
          : "Submitted. Score: " + result.score;
        $("submit-btn").disabled = true;
        // Refresh tasks to reflect unlock of next phase.
        return loadTasks().then(function () {
          return loadStatus();
        });
      })
      .then(function (status) {
        // After submission, show completion/return-later or go home.
        if (status.has_future_assessments) {
          showComplete(
            "Part complete",
            "You have completed this part. Please return later for the next assessment.",
          );
        } else {
          showComplete(
            "Study complete",
            "You have completed the study. Thank you!",
          );
        }
      })
      .catch(function (err) {
        statusEl.className = "status err";
        statusEl.textContent = err.message || "Submission failed.";
        $("submit-btn").disabled = false;
      });
  }

  // ---- AI chat ----
  function sendAiMessage() {
    var input = $("ai-input");
    var msg = input.value.trim();
    if (!msg) return;
    var task = state.currentTask;
    var chat = $("ai-chat");
    var statusEl = $("ai-status");

    var userMsg = document.createElement("div");
    userMsg.className = "ai-msg user";
    userMsg.textContent = msg;
    chat.appendChild(userMsg);
    input.value = "";
    statusEl.hidden = true;

    post("/ai/chat", { attempt_id: task.attempt_id, message: msg })
      .then(function (data) {
        var aiMsg = document.createElement("div");
        aiMsg.className = "ai-msg assistant";
        aiMsg.textContent = data.response;
        chat.appendChild(aiMsg);
        chat.scrollTop = chat.scrollHeight;
        updateAiRemaining(data.remaining_interactions);
        if (data.remaining_interactions <= 0) {
          $("ai-input").disabled = true;
          statusEl.className = "status";
          statusEl.textContent = "AI interaction limit reached.";
          statusEl.hidden = false;
        }
      })
      .catch(function (err) {
        statusEl.className = "status err";
        statusEl.textContent = err.message || "AI request failed.";
        statusEl.hidden = false;
      });
  }

  // ---- Completion ----
  function showComplete(title, message) {
    $("complete-title").textContent = title;
    $("complete-message").textContent = message;
    showScreen("complete");
  }

  // ---- Entry ----
  function enterStudy(code) {
    clearError($("entry-error"));
    ensureLearner(code)
      .then(function (learner) {
        state.learnerId = learner.id;
        state.learner = learner;
        saveLearnerId(learner.id);
        return loadTasks();
      })
      .then(function () {
        renderHome();
        showScreen("home");
      })
      .catch(function (err) {
        showError(
          $("entry-error"),
          err.message || "Could not load participant.",
        );
      });
  }

  // ---- Wire up ----
  $("entry-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var code = $("participant-code").value.trim();
    if (!code) return;
    enterStudy(code);
  });

  $("submit-btn").addEventListener("click", submitCurrent);

  $("back-btn").addEventListener("click", function () {
    stopTimer();
    loadTasks().then(function () {
      renderHome();
      showScreen("home");
    });
  });

  $("ai-form").addEventListener("submit", function (e) {
    e.preventDefault();
    sendAiMessage();
  });

  // ---- Boot ----
  var saved = loadLearnerId();
  if (saved) {
    enterStudy(saved);
  } else {
    showScreen("entry");
  }
})();
