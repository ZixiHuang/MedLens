
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

  init() {
    document
      .getElementById("body-condition-text")
      .addEventListener("keydown", this.handleBodyConditionKeyDown.bind(this));
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