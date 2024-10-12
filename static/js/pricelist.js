function add_to_cart(pid) {

	let td = document.getElementById('counter_container_' + pid)

	let xhr = new XMLHttpRequest()
	xhr.open('POST', '/add_product_to_cart', true)
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
	xhr.responseType = "json"

	xhr.onload = () => {
		if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {

			td.innerHTML = `<input class="pl_count" id="count-${pid}" type="number" value="1" onchange="update_count(${pid})">`

		}
	};

    xhr.send(`pid=${pid}`);

}


function update_count(pid) {
	let value = document.getElementById(`count-${pid}`).value

	let xhr = new XMLHttpRequest()
	xhr.open('POST', '/update_product_count_on_cart', true)
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded")
	xhr.responseType = "json"

    xhr.send(`pid=${pid}&count=${value}`);
}
