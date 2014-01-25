$(document).ready ->
  new FormSubmitter(".ui.form", "POST", ".", (response) -> console.log(response))
