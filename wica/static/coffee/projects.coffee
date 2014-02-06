$(document).ready ->
  submitter = new FormSubmitter(".ui.form", "POST", ".", (response) -> window.location.assign response)
