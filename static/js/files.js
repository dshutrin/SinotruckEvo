function remove_document(doc_id) {
    let xhr = new XMLHttpRequest();

    xhr.open("POST", "/remove_document", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.responseType = "json"

    xhr.onload = () => {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

			document.getElementById(`doc-${doc_id}`).remove()

		}
	};

    xhr.send(`doc_id=${doc_id}`);

}

function remove_folder(f_id) {
	let xhr = new XMLHttpRequest();

    xhr.open("POST", "/remove_folder", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.responseType = "json"

    xhr.onload = () => {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

			document.getElementById(`folder-${f_id}`).remove()

		}
	};

    xhr.send(`folder_id=${f_id}`);
}
