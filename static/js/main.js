function checkAll(newValue) {
    const referenceCheckboxes = document.querySelectorAll("#referenceCheckbox")

    for (let i = 0; i < referenceCheckboxes.length; i++) {
        checkbox = referenceCheckboxes[i]
        checkbox.checked = newValue
    }
}
