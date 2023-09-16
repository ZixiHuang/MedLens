
class DrugLensApp {
  constructor() {
  }

  // render() {

  // }

  handleBodyConditionKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey && event.target.value.trim() !== "") {
      event.preventDefault();
      console.log(event.target.value.trim())
      event.target.value = "";
    }
  }

  // handleEditNoteKeyDown(event) {
  //   if (event.key === 'Enter' && !event.shiftKey && event.target.value.trim() !== "") {
  //     event.preventDefault();
  //     this.noteWall.toggleNote()
  //     this.noteWall.addNote(event.target.value.trim());
  //     event.target.value = "";
  //     this.renderNotes();
  //   }
  // }

  // handleNoteDoubleClick(event) {
  //   if (event.target.classList.contains("note-text")) {
  //     this.noteWall.toggleNote(event.target.textContent)
  //     this.renderNotes();
  //   }
  // }

  // handleDeleteClick(event) {
  //   if(event.target.classList.contains("delete-btn")) {
  //     this.noteWall.deleteNote(event.target.textContent);
  //     this.renderNotes(); 
  //   }
  // }
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
    // document
    //   .getElementById("notes-wall")
    //   .addEventListener("dblclick", this.handleNoteDoubleClick.bind(this));
      // document
      // .getElementById("notes-wall")
      // .addEventListener("keydown", this.handleEditNoteKeyDown(this));
      // document
      // .getElementsByClassName("delete-btn")
      // .addEventListener("click", this.handleDeleteClick(this));
   
  }
}

export default DrugLensApp;