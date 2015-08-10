{% comment %} 
Creates the HTML code for a slider component.
    Inputs : 
     - panel : 
           "panelId"     : Unique Id
           "displayName" : The title of the panel       
           "jsonName"    : The name of the parameter to be used in the REST calls. 
           "content"     : Content of the paenel
              "min"      : The min value of the slider
              "max"      : The max value of the slider
              "default"  : Default value

{% endcomment %}

function()
{
    // Append the html code to DOM
    $('#{{panel.panelId}}').append(" {% filter escapejs %} {% include "app/Panels/sliderPanelTemplate.html" %} {% endfilter %} ");

    // Activate the slider
    $('#{{panel.panelId}}InputId').slider({formatter: function(value) { return 'Current value: ' + value;} });

    // Make sure the slider is full width 
    $('#{{panel.panelId}}SliderId').css('width', '100%');

    // Build the viewmodel for ko.js
    var viewmodel = {};

    // Custom ko binding "sliderValueChanged" registration
    ko.bindingHandlers.sliderValueChanged = {
        init: function(element, valueAccessor) {
           $(element).on("change", function(sliderValues) {
              var value = valueAccessor(); // The binded ko model property we want to change.
              value(sliderValues.value.newValue);
           });
        }
    };

    var sliderDefaultValue = $('#{{panel.panelId}}InputId').slider('getValue');
    viewmodel.SliderValue= ko.observable(sliderDefaultValue);

    // The functions required to implement the interface required by the panel framework. 
    viewmodel.subscribeValueChanged = function(callback) {
         this.SliderValue.subscribe(callback) ;
    };
    viewmodel.selectedValueAsJSON = function() { return { '{{ panel.jsonName }}' : this.SliderValue()}};

    return viewmodel;
}


