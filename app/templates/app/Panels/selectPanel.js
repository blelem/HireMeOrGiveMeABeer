{% comment %} 
Creates the HTML code for a select component.
    Inputs : 
     - panel : 
           "panelId"       : Unique Id
           "displayName"   : The title of the panel   
           "jsonName"      : The name of the parameter to be used in the REST calls. 
           "content"       : A dictionnary containing the items to populate the select. 
                             Each item has a 'key' and a 'description'
{% endcomment %}


function () {
    // Append the html code to DOM
    $('#{{panel.panelId}}').append(" {% filter escapejs %} {% include "app/Panels/selectPanelTemplate.html" %} {% endfilter %} ");


    // Build the viewmodel for ko.js
    var viewmodel = {};

    // Prepare the option list
    viewmodel.Options = ko.observableArray([
        {% for key, values in panel.content.items %}
            { id	      : "{{ key }}" ,
              description : "{{ values.description }}" },
        {% endfor %}
    ]);

    // Observe the selected value
    viewmodel.Selected = ko.observable(viewmodel.Options()[0]);

    // The functions required to implement the interface required by the panel framework. 
    viewmodel.subscribeValueChanged = function(callback) {
         this.Selected.subscribe(callback) ;
    };
    viewmodel.selectedValueAsJSON = function() { return { '{{ panel.jsonName }}' : this.Selected().id }};

    return viewmodel;
}