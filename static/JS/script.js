
const terminatescripBtns = document.querySelectorAll(".terminatescripBtn")
// const removescripBtns = document.querySelectorAll(".removescripBtn")

const terminationWindow = document.querySelector(".confirmWindow")
const closeTerminationWin = document.querySelector(".stopTermination")
const scripToTerminate = document.querySelector(".continueBtn")


terminatescripBtns.forEach(function(btn){
    btn.addEventListener("click", function(event){
        // Display Confirmation Window

        terminationWindow.style.display = "flex"
        let scripPID = event.target.value
   
        // insert hidden value in Confirmation Window'
        scripToTerminate.value = scripPID

    })
})

// removescripBtns.forEach(function(btn){
//     btn.addEventListener("click", function(event){
//         // Display Confirmation Window

//         terminationWindow.style.display = "flex"
//         let scripPID = event.target.value
   
//         // insert hidden value in Confirmation Window'
//         scripToTerminate.value = scripPID

//     })
// })

closeTerminationWin.addEventListener("click", function(){

    terminationWindow.style.display = "none"

})

