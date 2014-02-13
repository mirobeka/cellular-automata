$(document).ready ->
  new FormSubmitter(".ui.update.form", "PUT", ".", (response) -> window.location.assign response)
  new FormSubmitter(".ui.delete.form", "DELETE", ".", (response) -> window.location.assign response)

