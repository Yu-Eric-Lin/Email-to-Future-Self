
// function deleteNote(noteId) { 
//     fetch('/delete-note', {
//         method: 'POST',
//         body: JSON.stringify({ 'noteId': noteId }),
//     }).then((_res) => {
//         window.location.href = "/";     // refresh the window
//     });
// }
// function deleteNote(noteId) { 
//     fetch("/delete-note", {
//         method: "POST",
//         body: JSON.stringify({ noteId: noteId }),
//     });

//     // Refresh the page
//     window.location.href = "/";
// }

// Function to hide alerts after a certain time
// function hideAlert() {
//     setTimeout(function() {
//         document.querySelector('.alert-success').style.display = 'none';
//     }, 8000); // 8 seconds = 8000 milliseconds
// }

async function deleteNote(noteId) {
    try {
        const response = await fetch("/delete-note", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ noteId: noteId }),
        });

        if (!response.ok) {
            throw new Error("Failed to delete note");
        }

        window.location.href = "/"; // refresh the window
    } catch (error) {
        console.error(error);
    }
}

