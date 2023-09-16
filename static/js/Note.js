class Note {

    static nextId = 1;

    constructor(text) {
        this.id = Note.nextId++; 
        this.text = text; 
        this.edit = false;  
    }

    toggle() {
        this.edit = !this.edit
        console.log("note toggled~")
    }

}
export default Note;