var errors = 0;
const left = document.querySelector(".left");
const right = document.querySelector(".right");
const cell_block = document.querySelector("#cell2");
const cells = document.querySelector("#cell1");
// right.addEventListener("onclick", () => {
//   console.log("lk");
//   cells.style.display = "none";
//   cell_block.style.display = "flex";
// });
// const ass = document.getElementById("add_ass");
// const pop = document.querySelector(".cont1");
// const input1 = document.getElementById("dropval");
// ass.onclick = () => {
//   if (pop.style.display == "none") {
//     pop.style.display = "flex";
//     input1.required = true;
//   } else {
//     pop.style.display = "none";
//     input1.required = false;
//   }
// };
// const place1 = document.getElementById("cont1input1");
// const place2 = document.getElementById("dropval");
// const editass = document.getElementById("edit_ass");
// const epopup = document.querySelector(".cont1");
// editass.onclick = () => {
//   if (epopup.style.display == "none") {
//     epopup.style.display = "flex";
//     epopup.display.backgrounImage =
//       "linear-gradient(to top, #d6f18c 20%, #9f6202 80%)";
//     place1.placeholder = "Edit assignment name";
//     place2.placeholder = "Edit maximum marks";
//   } else {
//     epopup.style.display = "none";
//     epopup.display.backgrounImage =
//       "linear-gradient(to top, #86377b 20%, #27273c 80%)";
//     place1.placeholder = "Assignment name";
//     place2.placeholder = "Maximum marks";
//   }
// };

function int(value) {
  return parseInt(value);
}

function checkValue(sender) {
  let max = sender.max;
  max = int(max);
  let value1 = sender.value;
  let class1 = sender.class;
  if (isNaN(value1)) {
    if ((value1 == "A") | (value1 == "a")) {
      if (sender.className == "cellserror") errors--;
      sender.className = "cells";
      sender.value = "A";
    } else {
      if (sender.className == "cells") errors++;
      sender.className = "cellserror";
    }
  } else {
    let value1 = int(sender.value);
    if ((value1 > max) | (value1 < 0)) {
      if (sender.className == "cells") errors++;
      sender.className = "cellserror";
    } else {
      if (sender.className == "cellserror") errors--;
      sender.className = "cells";
    }
  }
  console.log(errors);
}

function validateMyForm(event) {
  // alert("Error="+errors)
  // console.log('hi');
  if (errors != 0) {
    alert("Invalid marks");
    event.preventDefault();
    // preve
    return false;
  }

  // alert("validations passed");
  return true;
}

// const err = document.getElementById(err);
// err.addEventListener('onclick', () => {
//   if (err != 0) alert('cuhutuia')
// })
let gradebtn = document.getElementById("gradepopupbtn");
let gradediv = document.getElementById("gradediv");
gradebtn.onclick = () => {
  if (gradediv.style.display == "none") {
    gradediv.style.display = "flex";
  } else {
    gradediv.style.display = "none";
  }
};
