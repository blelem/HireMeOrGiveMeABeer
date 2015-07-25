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


    // Append the html code to DOM
    $('#{{panel.panelId}}').append(" {% filter escapejs %} {% include "app/Panels/selectPanelTemplate.html" %} {% endfilter %} ");

    // Prepare the option list
    self.{{ panel.jsonName }}Options = ko.observableArray([
			{% for key, values in panel.content.items %}
				{ id	      : "{{ key }}" ,
				  description : "{{ values.description }}" },
			{% endfor %}
    ]);

    // Observe the selected value
    self.{{ panel.jsonName }}Selected = ko.observable(self.{{ panel.jsonName }}Options()[0]);

    // Callback that returns the selected value
	self.jsonData.push ( function() { return { '{{ panel.jsonName }}' : viewModel.{{ panel.jsonName }}Selected().id }});