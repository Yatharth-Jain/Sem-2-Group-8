var errors = 0;


function int(value) {
    return parseInt(value);
}

function checkValue(sender) {
    let max = sender.max;
    max = int(max);
    let value1 = sender.value;
    // console.log(value1+" "+max);
    let class1 = sender.class;
    if (isNaN(value1)) {
        if (value1 == 'A' | value1 == 'a') {
            if (sender.className == 'cellserror')
                errors--;
            sender.className = 'cells';
            sender.value = 'A';
        }
        else {
            if (sender.className == 'cells')
                errors++;
            sender.className = 'cellserror';
        }
    }
    else {
        let value1 = int(sender.value);
        if (value1 > max | value1 < 0) {
            if (sender.className == 'cells')
                errors++;
            sender.className = 'cellserror';

        }
        else {
            if (sender.className == 'cellserror')
                errors--;
            sender.className = 'cells';
        }
    }
    // console.log(errors)
}


function validateMyForm(event) {

    // alert("Error="+errors)
    // console.log('hi');
    if (errors != 0) {
        alert("Invalid marks");
        event.preventDefault()
        // preve
        return false;
    }

    // alert("validations passed");
    return true;
}

function checknums() {
    let vals=document.querySelectorAll('input.cells')
    vals.forEach((item) => checkValue(item));
}

checknums()
console.log(errors)