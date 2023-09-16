import NoteWall from "./NoteWall.js";

class StickyNoteApp {
  constructor() {
    this.noteWall = new NoteWall();
  }

  renderNotes() {
    // const visibleTodos = this.todoList.getVisibleTodos(this.filter);
    const noteWallElement = document.getElementById("notes-wall");
    noteWallElement.innerHTML = "";
    const notes = this.noteWall.getAllNotes()

    notes.forEach((note) => {
      // log(note.text)

      const noteElement = document.createElement("div");
      noteElement.className = "relative w-40 h-40 p-0 m-2 overflow-y-auto transition-transform transform bg-yellow-200 shadow-lg note hover:scale-105";
      
      const deleteButton = document.createElement("button")
      deleteButton.className = "absolute w-5 h-5 leading-5 text-center transition-opacity opacity-0 cursor-pointer delete-btn top-1 right-1 hover:opacity-100"
      deleteButton.textContent = "🗑";
      
      const noteText = document.createElement("div");
      noteText.className = "p-4 note-text";
      noteText.textContent = note.text;

      const noteEdit = document.createElement("input");
      noteEdit.className = "absolute top-0 left-0 w-full h-full p-4 transition-transform transform bg-yellow-300 shadow-xl resize-none outline-rose-700 outline-offset-0 note-edit note hover:scale-105";
      noteEdit.value = note.text;

      if (note.edit == true) {
        noteText.classList.add("hidden");
      } else {
        noteEdit.classList.add("hidden"); 
      }

      noteElement.appendChild(noteText);
      noteElement.appendChild(deleteButton);
      noteElement.appendChild(noteEdit)
      noteWallElement.appendChild(noteElement);
    });

  }

  handleNewNoteKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey && event.target.value.trim() !== "") {
      event.preventDefault();
      this.noteWall.addNote(event.target.value.trim());
      event.target.value = "";
      this.renderNotes();
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

  handleNoteDoubleClick(event) {
    if (event.target.classList.contains("note-text")) {
      this.noteWall.toggleNote(event.target.textContent)
      this.renderNotes();
    }
  }

  // handleDeleteClick(event) {
  //   if(event.target.classList.contains("delete-btn")) {
  //     this.noteWall.deleteNote(event.target.textContent);
  //     this.renderNotes(); 
  //   }
  // }

  init() {
    document
      .getElementById("new-note")
      .addEventListener("keydown", this.handleNewNoteKeyDown.bind(this));
    document
      .getElementById("notes-wall")
      .addEventListener("dblclick", this.handleNoteDoubleClick.bind(this));
      // document
      // .getElementById("notes-wall")
      // .addEventListener("keydown", this.handleEditNoteKeyDown(this));
      // document
      // .getElementsByClassName("delete-btn")
      // .addEventListener("click", this.handleDeleteClick(this));
   

    this.renderNotes();
  }
}

export default StickyNoteApp;