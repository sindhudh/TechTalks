const Imagecontainer = document.querySelector(".Imagecontainer")
for(let i =1; i<501; i++){
    const image = document.createElement("img")
    image.setAttribute("src",`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${i}.png`)
    image.classList.add("iamgesclass")
    Imagecontainer.append(image)
}