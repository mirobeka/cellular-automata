$(document).ready ->
  new FormSubmitter(".ui.form", "POST", ".", (response) -> window.location.assign response)
