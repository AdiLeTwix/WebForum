function deleteNote(noteId) {
    var id = parseInt(noteId)
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: id }),
    }).then((_res) => {
        window.location.href = "/my";
    });
}

function deleteCode(codeID) {
    var id = parseInt(codeID)
    fetch("/remove-code", {
        method: "POST",
        body: JSON.stringify({ codeID: id }),
    }).then((_res) => {
        window.location.href = "/manage-code";
    });
}