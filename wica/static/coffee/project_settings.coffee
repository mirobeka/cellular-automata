addOption = (event) ->
    section = $(event.target).attr('data-section')

    # get input tag with name of new option
    inputTag = $(event.target).siblings('input[name="optionName"]').get(0)

    # get option name
    option = $(inputTag).val()

    console.log "Adding option #{option} in section #{section}"

    # clear value in input tag
    $(inputTag).val("")

    opt = optionHtml(section, option)
    insertOption(section, opt)

addSection = (event) ->
    inputTag = $(event.target).siblings('input[name="sectionName"]').get(0)

    console.log inputTag
    section = $(inputTag).val()

    console.log "adding section #{section}"
    sct = sectionHtml(section)
    # clear input field for section
    $(inputTag).val("")
    insertSection(sct)

removeOption = (event) ->
    section = $(event.target).attr('data-section')
    option = $(event.target).attr('data-option')
    console.log "removing #{section}.#{option}"
    $(".#{section} > .#{option}").remove()


# function for generating option in specified section of project
# configuration
optionHtml = (section, option) ->
    """<div class="field #{option}">
    <label>#{option}</label>
    <div class="ui action input">
        <input type="text" name="#{section}.#{option}" placeholder="Enter value">
        <div class="ui removeOption tiny red button" data-option="#{option}" data-section="#{section}">
            <i class="ui minus icon"></i>
        </div>
    </div>
    </div>"""

# function for generating whole section for project configuration
sectionHtml = (section) ->
    """
    <div class="ui horizontal icon divider">
      <i class="ellipsis horizontal icon"></i>
    </div>
    <div class="#{section} last">

        <h3>#{section}</h3>

          <div class="ui three column grid">
            <div class="column">
              <div class="ui action input">
                <input type="text" name="optionName" placeholder="Option name">
                <div class="ui addOption button" data-section="#{section}">
                    <i class="ui plus icon"></i>
                </div>
              </div>
            </div>

          </div>"""

insertOption = (section, htmlToInsert) ->
    section = $(".#{section}")

    newOption = $(htmlToInsert)
    newOption.bind("click", addOption)
    newOption.insertBefore(section.find(".ui.three.column.grid"))

insertSection = (htmlToInsert) ->
    lastSection = $(".last")

    newSection = $(htmlToInsert)

    newSection.insertAfter(".last")
    newSection.find(".ui.addOption.button").bind("click", addOption)



    lastSection.removeClass('last')

$(document).ready ->
    # creates form submitters for deleting configuration and updating configuration
    new FormSubmitter(".ui.update.form", "PUT", ".", (response) -> window.location.assign response)
    new FormSubmitter(".ui.delete.form", "DELETE", ".", (response) -> window.location.assign response)

    # button for adding fields
    $('.addSection').bind('click', addSection)
    $('.addOption').bind('click', addOption)
    $('.removeOption').bind('click', removeOption)

