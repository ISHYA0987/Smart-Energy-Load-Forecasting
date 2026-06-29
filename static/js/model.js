document.addEventListener("DOMContentLoaded", () => {

    console.log("Model Page Loaded");

});
document.querySelectorAll(".node").forEach((node,index)=>{

    node.style.animationDelay = `${index*0.15}s`;

});