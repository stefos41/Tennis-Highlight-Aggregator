document.addEventListener("DOMContentLoaded", function () {
  const addButton = document.getElementById("add-highlight");
  const statusDiv = document.getElementById("status");
  const videoInfoDiv = document.getElementById("video-info");

  // Helper function to format duration
  function formatDuration(seconds) {
    if (!seconds) return "0:00";
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? "0" : ""}${remainingSeconds}`;
  }

  // Show loading state
  function showLoading() {
    videoInfoDiv.style.opacity = "0.5";
    addButton.disabled = true;
    statusDiv.textContent = "Loading...";
    statusDiv.className = "status-message loading";
  }

  // Hide loading state
  function hideLoading() {
    videoInfoDiv.style.opacity = "1";
  }

  // Show status message
  function showStatus(message, type = "") {
    statusDiv.textContent = message;
    statusDiv.className = "status-message " + type;
  }

  // Get current YouTube URL from active tab
  chrome.tabs.query(
    { active: true, currentWindow: true },
    async function (tabs) {
      try {
        const url = tabs[0]?.url;
        if (!url) {
          showStatus("No active tab found", "error");
          return;
        }

        const isYouTubeUrl = url.match(/youtube\.com\/watch|youtu\.be\/|youtube\.com\/embed\//);
        if (!isYouTubeUrl) {
          showStatus("Please navigate to a YouTube video page", "error");
          return;
        }

        showLoading();
        const videoInfo = await fetchVideoInfo(url);
        if (videoInfo) {
          displayVideoInfo(videoInfo);
          setupAddButton(videoInfo);
        }
      } catch (error) {
        showStatus(`Error: ${error.message}`, "error");
      } finally {
        hideLoading();
      }
    }
  );

  // Fetch video info from backend API
  async function fetchVideoInfo(url) {
    try {
      const response = await fetch(
        `${Config.API_BASE_URL}/video-info?url=${encodeURIComponent(url)}`,
        { headers: { "api-key": Config.API_KEYS[0] } }
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to fetch video info");
      }
      return await response.json();
    } catch (error) {
      console.error("Fetch error:", error);
      throw new Error("Failed to connect to the server");
    }
  }

  // Display video information
  function displayVideoInfo(videoInfo) {
    document.getElementById("video-title").textContent = videoInfo.title || "No title available";
    document.getElementById("video-channel").textContent = videoInfo.channel || "Unknown channel";
    document.getElementById("video-duration").textContent = formatDuration(videoInfo.duration);
  }

  // Set up the add button
  function setupAddButton(videoData) {
    addButton.disabled = false;
    addButton.addEventListener("click", async () => {
      try {
        addButton.disabled = true;
        showStatus("Adding highlight...", "loading");

        const response = await fetch(`${Config.API_BASE_URL}/add-highlight`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "api-key": Config.API_KEYS[0],
          },
          body: JSON.stringify(videoData),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || "Failed to add highlight");
        }

        showStatus("Highlight added successfully!", "success");
        addButton.disabled = true;
      } catch (error) {
        showStatus(`Error: ${error.message}`, "error");
        addButton.disabled = false;
      }
    });
  }
});