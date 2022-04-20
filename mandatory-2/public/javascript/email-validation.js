const remove_errors = (id) => {
    const error_prompt = document.getElementById(id)
    if (error_prompt) {
        error_prompt.remove();
    }
}

const toggle_spinner = () => {
    document.querySelector(`#submit-text`).classList.toggle('hidden')
    document.querySelector('.spinner').classList.toggle('hidden')
}

let in1 = document.getElementById('otc-1');
let ins = document.querySelectorAll('input[type="number"]');
let splitNumber = function(e) {
    let data = e.data || e.target.value;
    if ( ! data ) return;
    if ( data.length === 1 ) return;
    popuNext(e.target, data);
}
let popuNext = function(el, data) {
    el.value = data[0]; // Apply first item to first input
    data = data.substring(1); // remove the first char.
    if ( el.nextElementSibling && data.length ) {
        // Do the same with the next element and next data
        popuNext(el.nextElementSibling, data);
    }
};

ins.forEach(function(input) {
	/**
	 * Control on keyup to catch what the user intent to do.
	 * I could have check for numeric key only here, but I didn't.
	 */
	input.addEventListener('keyup', function(e){
		// Break if Shift, Tab, CMD, Option, Control.
		if (e.keyCode === 16 || e.keyCode == 9 || e.keyCode == 224 || e.keyCode == 18 || e.keyCode == 17) {
			 return;
		}
		
		// On Backspace or left arrow, go to the previous field.
		if ( (e.keyCode === 8 || e.keyCode === 37) && this.previousElementSibling && this.previousElementSibling.tagName === "INPUT" ) {
			this.previousElementSibling.select();
		} else if (e.keyCode !== 8 && this.nextElementSibling) {
			this.nextElementSibling.select();
		}
		
		// If the target is populated to quickly, value length can be > 1
		if ( e.target.value.length > 1 ) {
			splitNumber(e);
		}
	});
	
	/**
	 * Better control on Focus
	 * - don't allow focus on other field if the first one is empty
	 * - don't allow focus on field if the previous one if empty (debatable)
	 * - get the focus on the first empty field
	 */
	input.addEventListener('focus', function(e) {
		// If the focus element is the first one, do nothing
		if ( this === in1 ) return;
		
		// If value of input 1 is empty, focus it.
		if ( in1.value == '' ) {
			in1.focus();
		}
		
		// If value of a previous input is empty, focus it.
		// To remove if you don't wanna force user respecting the fields order.
		if ( this.previousElementSibling.value == '' ) {
			this.previousElementSibling.focus();
		}

        input.addEventListener('focus', function(e) {
            // If the focus element is the first one, do nothing
            if ( this === in1 ) return;
            
            // If value of input 1 is empty, focus it.
            if ( in1.value == '' ) {
                in1.focus();
            }
            
            // If value of a previous input is empty, focus it.
            // To remove if you don't wanna force user respecting the fields order.
            if ( this.previousElementSibling.value == '' ) {
                this.previousElementSibling.focus();
            }
        });
	});
});


// Handle copy/paste of a big number.
// It catches the value pasted on the first field and spread it into the inputs.
in1.addEventListener('input', splitNumber);

document.getElementById('validation-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    toggle_spinner();
    remove_errors('login_error_prompt');
    
    let code = ""
    for (let input of document.querySelectorAll('input[type=number]')){
        code += input.value;
        input.value = '';
    };

    const data = {
        code: Number(code),
        user_email: document.getElementById('validation-email').value
    }
    const response = await fetch(location.pathname, {
        method: 'POST',
        credentials: 'same-origin',
        mode: 'no-cors',
        cache: 'no-cache',
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json'
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });

    if ( response.ok ){
        console.log('successfully validated email');
        location = ('/login')
    } else {
        const body = await response.json()
        console.log(body);
        const error_prompt = document.createElement('span');
        error_prompt.id = 'login_error_prompt';
        error_prompt.classList.add('error_prompt');
        error_prompt.innerHTML = body.msg;
        document.getElementById('error-container').prepend(error_prompt)
    }
    toggle_spinner();
});

document.querySelector('#resend-btn').addEventListener('click', async (e) => {
    e.preventDefault();

    const data = {
        user_email: document.getElementById('validation-email').value,
        user_name: document.getElementById('validation-user_name').value
    }

    await fetch(`${location.pathname}/resend`, {
        method: 'POST',
        credentials: 'same-origin',
        mode: 'no-cors',
        cache: 'no-cache',
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json'
        },
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });

});