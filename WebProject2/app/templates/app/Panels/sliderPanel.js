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

// Append the html code to DOM
$('#{{panel.panelId}}').append(" {% filter escapejs %} {% include "app/Panels/sliderPanelTemplate.html" %} {% endfilter %} ");

// Activate the slider
self.{{panel.panelId}} = $('#{{panel.panelId}}InputId').slider({
    formatter: function(value) {
    		return 'Current value: ' + value;
    }   
});

// Make sure the slider is full width 
$('#{{panel.panelId}}SliderId').css('width', '100%');

{{panel.panelId}}SliderId

// Callback that returns the selected value
self.jsonData.push ( function() { 
    return { '{{ panel.jsonName }}' : self.{{panel.panelId}}.slider('getValue') }
});

