let uprange=document.querySelectorAll('.upperlimit');

let inputs=document.querySelectorAll('div.input-group input');
for (let i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener("input",()=>valuecheck(inputs[i],i));
}

errors=0;

function valuecheck(element,ind) {
    let val=element.value;
    let ur=parseInt(uprange[ind].innerHTML);
    let lre=uprange[ind+1];
    if(val > ur | val<0){
        if (element.style.color=="black")errors++;
        element.style.color="red"
    }
    else if(val==0 | val==1){
        element.style.color="black"
        for(let i=ind+1;i<inputs.length;i++){
            if(inputs[i].style.color=='red'){
                errors--;
                inputs[i].style.color=='black';
            }
            inputs[i].value=0;
            uprange[i].innerHTML=0;
        }
    }
    else{
        if(element.style.color=='red')errors--;
        element.style.color="black"
        lre.innerHTML=val-1;
    }
}

function checkform(event) {
    if(errors!=0){
        alert("Range is not correct");
        event.preventDefault();
    }
}