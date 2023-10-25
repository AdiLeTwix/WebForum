function deleteNote(noteId) {
    var id = parseInt(noteId)
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: id }),
    }).then((_res) => {
        window.location.href = "/my";
    });
}