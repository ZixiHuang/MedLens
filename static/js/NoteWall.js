import Note from "./Note.js";

// export const FILTERS = {
//   ALL: "all",
//   ACTIVE: "active",
//   COMPLETED: "completed",
// };

class NoteWall {
  constructor() {
    this.notes = [];
  }

  addNote(text) {
    const note = new Note(text);
    this.notes.push(note);
  }

  toggleNote(noteText) {
    console.log("finding note", noteText)
    const note = this.notes.find((t) => t.text === noteText);
    if (note) {
      note.toggle();
    }
  }
  
  deleteNote(noteText) {
    function findText(text) {
      return text === noteText;
    }
    notes = notes.filter(findText)
  }



  getAllNotes() {
    return this.notes
  }

//   getVisibleTodos(filter) {
//     switch (filter) {
//       case FILTERS.ACTIVE:
//         return this.todos.filter((todo) => !todo.completed);
//       case FILTERS.COMPLETED:
//         return this.todos.filter((todo) => todo.completed);
//       default:
//         return this.todos;
//     }
//   }

//   markAllAsComplete() {
//     this.todos.forEach((todo) => (todo.completed = true));
//   }

//   clearCompleted() {
//     this.todos = this.todos.filter((todo) => !todo.completed);
//   }

//   getActiveTodoCount() {
//     return this.todos.filter((todo) => !todo.completed).length;
//   }
}

export default NoteWall;