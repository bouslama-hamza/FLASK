function menutoogle(){
    const app = document.querySelector("#app_profile")
    const manage = document.querySelector(".manage_account_picture")
    const data_base = document.querySelector(".data_base_aproved")
    const data_pie = document.querySelector(".data_base_pie")
    app.classList.toggle('active')
    manage.classList.toggle('active')
    data_base.classList.toggle('active')
    data_pie.classList.toggle('active')
}
function submit(){
    document.submit.submit()
}