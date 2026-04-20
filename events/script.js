const colorInput = document.getElementById("color");
colorInput.addEventListener('change', () => {
    const colorNew = document.createElement('div');
    colorNew.style.backgroundColor = `${colorInput.value}`;
    colorNew.classList = 'controlPanel-colorPanel-saveConteiner-colorsSaved';
    console.log(colorNew);
    document.getElementById('colorSaved').appendChild(colorNew);
});