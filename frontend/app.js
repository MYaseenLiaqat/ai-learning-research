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
    material: $("screen-material"),
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
        return "Supported practice";
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
    var d = parseServerTimestamp(iso);
    return d.toLocaleString();
  }

  function parseServerTimestamp(value) {
    if (!value) return new Date(value);
    if (/[zZ]|[+-]\d{2}:?\d{2}$/.test(value)) {
      return new Date(value);
    }
    return new Date(value + "Z");
  }

  // ---- Identity ----
  // Longitudinal experiment: participants must return using the same learner
  // record so their randomized condition and measurement arm stay stable.
  // We only LOAD an existing learner by numeric code. We never auto-create.
  function ensureLearner(code) {
    var numeric = /^\d+$/.test(code);
    if (!numeric) {
      return Promise.reject(
        new Error(
          "Invalid participant code. Please enter the numeric code provided by the researcher.",
        ),
      );
    }
    return get("/learners/" + code).then(function (learner) {
      return learner;
    });
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

  function appendBasicMarkdown(parent, text) {
    var codeBlock = null;
    String(text || "")
      .replace(/([^\n])\s+(?=#{1,6}\s+)/g, "$1\n")
      .split("\n")
      .forEach(function (line) {
        if (line.trim().indexOf("```") === 0) {
          if (codeBlock) {
            parent.appendChild(codeBlock);
            codeBlock = null;
          } else {
            codeBlock = document.createElement("pre");
          }
          return;
        }
        if (codeBlock) {
          codeBlock.textContent += (codeBlock.textContent ? "\n" : "") + line;
          return;
        }
        if (!line.trim()) return;

        var heading = line.match(/^(#{1,6})\s+(.+)$/);
        var block = document.createElement(
          heading ? "h" + heading[1].length : "p",
        );
        var content = heading ? heading[2] : line;
        var parts = content.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);

        parts.forEach(function (part) {
          if (
            part.indexOf("**") === 0 &&
            part.lastIndexOf("**") === part.length - 2
          ) {
            var strong = document.createElement("strong");
            strong.textContent = part.slice(2, -2);
            block.appendChild(strong);
          } else if (
            part.indexOf("`") === 0 &&
            part.lastIndexOf("`") === part.length - 1
          ) {
            var code = document.createElement("code");
            code.textContent = part.slice(1, -1);
            block.appendChild(code);
          } else {
            block.appendChild(document.createTextNode(part));
          }
        });

        parent.appendChild(block);
      });
    if (codeBlock) parent.appendChild(codeBlock);
  }

  // ---- Rendering: learning material ----
  function renderMaterial() {
    return get("/learning/loops?learner_id=" + state.learnerId).then(
      function (module) {
        var container = $("material-content");
        container.innerHTML = "";

        function section(title, text) {
          var h = document.createElement("h3");
          h.textContent = title;
          container.appendChild(h);
          appendBasicMarkdown(container, text);
        }

        section("Concept explanation", module.explanation);
        if (module.worked_example) {
          section("Worked example", module.worked_example.problem);
          var sol = document.createElement("pre");
          sol.textContent = module.worked_example.solution || "";
          container.appendChild(sol);
        }
        if (module.guided_practice) {
          section("Guided practice", module.guided_practice.problem);
        }
        if (module.static_hints && module.static_hints.length) {
          section("Hints", module.static_hints.join("\n"));
        }
      },
    );
  }

  function startSupportedSession() {
    var btn = $("start-supported-btn");
    clearError($("material-error"));
    btn.disabled = true;
    btn.textContent = "Starting...";
    return post("/learning/loops/start?learner_id=" + state.learnerId, null)
      .then(function () {
        clearError($("material-error"));
        return loadTasks();
      })
      .catch(function (err) {
        btn.disabled = false;
        btn.textContent = "Start Supported session";
        throw err;
      });
  }

  function goToHome() {
    loadTasks()
      .then(function () {
        renderHome();
        showScreen("home");
      })
      .catch(function () {
        var statusEl = $("submit-status");
        statusEl.className = "status err";
        statusEl.textContent =
          "We could not load your tasks. Please try again.";
        statusEl.hidden = false;
      });
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
        openTask(t).catch(function (err) {
          showError($("home-message"), err.message || "Could not start task.");
        });
      });
      card.appendChild(btn);

      list.appendChild(card);
    });
  }

  // ---- Rendering: task ----
  function renderTask(task) {
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

  function openTask(task) {
    if (task.type === "supported") {
      renderTask(task);
      return Promise.resolve(task);
    }
    return post(
      "/tasks/" + task.id + "/start?learner_id=" + state.learnerId,
      null,
    ).then(function (startedTask) {
      renderTask(startedTask);
      return startedTask;
    });
  }

  function startTimer(expiresIso) {
    stopTimer();
    var timerEl = $("task-timer");
    function tick() {
      var now = Date.now();
      var expires = parseServerTimestamp(expiresIso).getTime();
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
    $("ai-remaining").textContent = remaining + " AI requests remaining";
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
        return loadTasks()
          .then(function () {
            return loadStatus();
          })
          .then(function (status) {
            // After submission, if Immediate is now available, guide the
            // participant straight into it (still AI-free). Otherwise show
            // completion/return-later or study-complete.
            var immediate = state.tasks.find(function (t) {
              return t.type === "immediate";
            });
            if (immediate) {
              openTask(immediate).catch(function () {
                statusEl.className = "status err";
                statusEl.textContent =
                  "Your submission was recorded, but the next assessment could not be opened. Please return to the task list and try again.";
                statusEl.hidden = false;
              });
              return;
            }
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
          .catch(function () {
            statusEl.className = "status err";
            statusEl.textContent =
              "Your submission was recorded, but we could not refresh the task list. Please try again.";
            statusEl.hidden = false;
          });
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
        appendBasicMarkdown(aiMsg, data.response);
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
        // If the Supported session has not started, show the standardized
        // learning material first. Otherwise resume at the task list.
        var supported = state.tasks.find(function (t) {
          return t.type === "supported" && !t.started_at;
        });
        if (supported) {
          return renderMaterial().then(function () {
            $("start-supported-btn").disabled = false;
            $("start-supported-btn").textContent = "Start Supported session";
            showScreen("material");
          });
        }
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
    var btn = $("entry-btn");
    btn.disabled = true;
    btn.textContent = "Loading...";
    enterStudy(code).finally(function () {
      btn.disabled = false;
      btn.textContent = "Continue";
    });
  });

  $("start-supported-btn").addEventListener("click", function () {
    startSupportedSession()
      .then(function (tasks) {
        var supported = tasks.find(function (task) {
          return task.type === "supported";
        });
        if (supported) {
          return openTask(supported);
        } else {
          goToHome();
        }
      })
      .catch(function (err) {
        var el = $("material-error");
        showError(el, err.message || "Could not start the supported session.");
      });
  });

  $("submit-btn").addEventListener("click", submitCurrent);

  $("back-btn").addEventListener("click", function () {
    stopTimer();
    goToHome();
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
