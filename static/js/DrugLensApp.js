
class DrugLensApp {
  constructor() {
    this.socket = io.connect('http://' + document.domain + ':' + location.port);
    this.socket.on('openai_task_started', function(data) {
        console.log("task started");
        const liveWindow = document.getElementById("live-window");
        const picInstruction = document.getElementById("take-picture-instruction");
        const loadingAnime = document.getElementById("loading");
        liveWindow.style.display = "none";
        loadingAnime.style.display = "flex";
        picInstruction.style.display = "none"; 
    });
  }

  async fetchUpdatedData() {
    try {
        const response = await fetch('/get-updated-response');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        if (data === null || data.length === 0) {
          return;
        }
        // Do something with the data, e.g., update the DOM or store it in a variable
        console.log(data);
        const instructionDiv = document.getElementById("instruction-section");
        instructionDiv.textContent = data[0];
        // Make an AJAX request to the Flask route to synthesize audio
        const synthResponse = await fetch('/synthesize', {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify({ text: data[0] })
        });

        if (!synthResponse.ok) {
            throw new Error(`HTTP error during synthesis! Status: ${synthResponse.status}`);
        }

        const synthData = await synthResponse.json();
        const audioDataUri = synthData.audio_data_uri;
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = audioDataUri;
        audioPlayer.play();
    } catch (error) {
        console.error("Error fetching updated data:", error);
    }
}


  handleBodyConditionKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey && event.target.value.trim() !== "") {
      event.preventDefault();
      console.log(event.target.value.trim())
      event.target.value = "";
    }
  }

  handleGetTeamInfo() {
    const information = document.getElementById("info")
    information.innerHTML = "<p> We are a Hophacks 2023 team composed of Chujian Yu, Lance Lian, Joanna Cheng and Kevin Huang</p> "
  }

  handleGetHomeInfo() {
    const information = document.getElementById("info")
    information.innerHTML = ""
  }

  handleGetAboutInfo() {
    const information = document.getElementById("info")
    information.innerHTML = "<p> This is an app that helps you to get instruction on a medication simply by taking a photo of the bottle </p>"
  }

  handleTakeImage() {
    const liveWindow = document.getElementById("live-window")
    liveWindow.classList.add("center-container")
    liveWindow.classList.remove("hidden")
    const instruction = document.getElementById("take-picture-instruction")
    instruction.classList.remove("hidden") 
    instruction.classList.add("center-container")
  }

  handleSpeech() {
    const text = "what is the temperature in Sydney";
      const speechSynthesis = window.speechSynthesis;

      if (speechSynthesis) {
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
      } else {
        alert('Text-to-speech is not supported in this browser.');
      }
      console.log("done speaking")
  }


  init() {
    
    document
      .getElementById("body-condition-text")
      .addEventListener("keydown", this.handleBodyConditionKeyDown.bind(this));
    document
      .getElementById("team")
      .addEventListener("click", this.handleGetTeamInfo.bind(this));
    document
      .getElementById("about")
      .addEventListener("click", this.handleGetAboutInfo.bind(this));
    document
      .getElementById("home")
      .addEventListener("click", this.handleGetHomeInfo.bind(this));
    document
      .getElementById("taking-img")
      .addEventListener("click", this.handleTakeImage.bind(this));
    document
      .getElementById("logo-img")
      .addEventListener("click", this.handleSpeech.bind(this));
    // document
    //   .getElementById("notes-wall")
    //   .addEventListener("dblclick", this.handleNoteDoubleClick.bind(this));
      // document
      // .getElementById("notes-wall")
      // .addEventListener("keydown", this.handleEditNoteKeyDown(this));
      // document
      // .getElementsByClassName("delete-btn")
      // .addEventListener("click", this.handleDeleteClick(this));
      this.fetchUpdatedData = this.fetchUpdatedData.bind(this);
      setInterval(this.fetchUpdatedData, 5000);

      
  }
}

export default DrugLensApp;