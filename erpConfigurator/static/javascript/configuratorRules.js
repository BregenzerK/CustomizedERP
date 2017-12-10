$(document).ready(function(){
	
	var configuratorRules;
	
	$.ajax({
        type: "GET",
        url: "/static/data/configuratorRules.xml",
        dataType: "xml",
        success: function(xml) {
        	 configuratorRules= $(xml);
        }
    });
	
	$(document).find('input:checkbox').change(function(){
		var changed = $(this);
		var tab = $('.ui.tab.active');
		var counter=0;
		
		if (changed.prop('checked')){
			verifyDependenciesSelect(changed);
			checkDependency(tab.attr('data-tab'));
		}else{
			verifyDependenciesUnselect(changed);
			tab.find('input:checkbox, input:radio').each(function(){
				if (checkState($(this))==true){
					counter+=1;
					
				}
			});
			
			if(counter==1){
				uncheckDependency(tab.attr('data-tab'));
			}
			
		}
		
	});
	
	$(document).find('input:radio').change(function(){
		var changed = $(this);
		var tab = $('.ui.tab.active');
		var counter=0;
		
		if (changed.val()=='True'){
			verifyDependenciesSelect(changed);
			checkDependency(tab.attr('data-tab'));
		}else{
			verifyDependenciesUnselect(changed);
			tab.find('input:checkbox, input:radio').each(function(){
				if (checkState($(this))==true){
					counter+=1;
				}
			});
			
			if(counter==1){
				uncheckDependency(tab.attr('data-tab'));
			}
			
		}
		
	});
	
	function checkState(obj){
		var result;
		
		if (($(obj).parent().hasClass('ui checkbox'))||($(obj).parent().hasClass('ui toggle checkbox')) ){
			result =  obj.parent().checkbox('is checked');
		}
		else {
			$(obj).each(function(){
				if($(this).is(':checked')){
					
					if (($(this).hasClass('radio'))&&($(this).val()=='True')){
						result= true;
					}else if (($(this).hasClass('radio'))&&($(this).val()=='False')){
						result= false;
					}else{
						console.log('wrong input for '+$(this).attr('name')+'! Value ='+$(this).val());
					}
				}
			});
		}
		return result;
	}
	
	function convertBool (obj){
		if (obj.toLowerCase() === 'true'){
			return true;	
		}else if (obj.toLowerCase() === 'false'){
			return false;
		}else {
			console.log("wrong input: "+obj.val());
		}

	}
	
	function verifyDependenciesSelect(changed){
		$(configuratorRules).find('rule').each(function(i,j) {
			if ($(j).find("if").text()==changed.attr('name')){
				$(j).find("check").each(function(){
					var dependency = $(this).text();
					checkDependency(dependency);
				});
				$(j).find("visible").each(function(){
					var dependency = $(this).text();
					visibleDependency(dependency);
				});
				
				$(j).find("enable").each(function(){
					var dependency = $(this).text();
					enableDependency(dependency);
				});
				
				if(($(j).find('and').length>0)&&($(j).find('and_check').length>0)||($(j).find('and_visible').length>0)||($(j).find('and_enable').length>0)){	
					var xml_and = $(j).find('and');
					var and_condition = $(document).find('[name='+xml_and.text()+']');
					var state = checkState(and_condition);
					var xml_value = xml_and.attr('value');
					if (typeof xml_value !== typeof undefined){
						xml_value= convertBool(xml_value);
					}else{
						xml_value=true;
					}
					if (state == xml_value){
						$(j).find('and_check').each(function(){
							var and_dependency = $(this).text();
							checkDependency(and_dependency);
						});
						$(j).find('and_visible').each(function(){
							var and_dependency = $(this).text();
							visibleDependency(and_dependency);
						});
						$(j).find('and_enable').each(function(){
							var and_dependency = $(this).text();
							enableDependency(and_dependency);
						});
					}
				}
			};
		});
	};
	
	function verifyDependenciesUnselect(changed){
		$(configuratorRules).find('rule').each(function(i,j) {
			if ($(j).find("if").text()==changed.attr('name')){	
				$(j).find("uncheck").each(function(){
					var dependency = $(this).text();
					uncheckDependency(dependency);
				});
				$(j).find("invisible").each(function(){
					var dependency = $(this).text();
					invisibleDependency(dependency);
				});
				
				$(j).find("disable").each(function(){
					var dependency = $(this).text();
					disableDependency(dependency);
				});
				
				if(($(j).find('and').length>0)&&($(j).find('and_uncheck').length>0)||($(j).find('and_invisible').length>0)||($(j).find('and_disable').length>0)){	
					var xml_and= $(j).find('and');
					var and_condition = $(document).find('[name='+xml_and.text()+']');
					var state = checkState(and_condition);
					var xml_value = xml_and.attr('value');
					if (typeof xml_value !== typeof undefined){
						xml_value= convertBool(xml_value);
					}else{
						xml_value=false;
					}
					if (state == xml_value){
						$(j).find('and_uncheck').each(function(){
							var and_dependency = $(this).text();
							uncheckDependency(and_dependency);
						});
						$(j).find('and_invisible').each(function(){
							var and_dependency = $(this).text();
							invisibleDependency(and_dependency);
						});
						$(j).find('and_disable').each(function(){
							var and_dependency = $(this).text();
							disableDependency(and_dependency);
						});
					}
				}
			};
		});
	};
	
	function checkDependency(dependency){
		var element = $(document).find('[name='+dependency+']');		
		var elementParent = element.parent();
		if((elementParent.hasClass('ui toggle checkbox'))||(elementParent.hasClass('ui checkbox'))){
			if(elementParent.checkbox('is checked')==false){
				elementParent.checkbox('check');
			}	
		}else if (element.hasClass('radio')){
			element[0].checked=true; 
		}else {
			console.log(dependency+' is not a checkbox or a radio button or is already checked');
		}
		
		
	};
	
	function uncheckDependency(dependency){
		var element = $(document).find('[name='+dependency+']');
		var elementParent = element.parent();
		if((elementParent.hasClass('ui toggle checkbox checked'))||(elementParent.hasClass('ui checkbox checked'))){
		
			if(elementParent.checkbox('is checked')){
				elementParent.checkbox('uncheck');
			}
			
		}else if (element.hasClass('radio')){
			element[1].checked = true;
			
		}else if (element.hasClass('ui segment')){
			element.find('input:checkbox:checked, input:radio:checked').each(function(){
			var dependencyUncheck = $(this).attr('name');
			uncheckDependency(dependencyUncheck);
			});
		}else {
			console.log(dependency+' is not a checkbox or a radio button or is already unchecked');
		}
	};
	
	function visibleDependency(dependency){
		$(document).find('[name='+dependency+']').removeAttr('hidden');
	};
	
	function invisibleDependency(dependency){
		var element = $(document).find('[name='+dependency+']');
		element.attr('hidden', 'hidden');
		element.find('input:checkbox:checked, input:radio:checked').each(function(){
			var dependencyUncheck = $(this).attr('name');
			uncheckDependency(dependencyUncheck);
		});
		element.find("[name*='_kontodaten']").attr('hidden', 'hidden');		//Blende zusätzlich Segment Kontodaten aus!
	};
	
	function enableDependency(dependency){
		var element = $(document).find('[name='+dependency+']');
		element.parent().checkbox('enable');
		
	}
	
	function disableDependency(dependency){
		
		var elementParent = $(document).find('[name='+dependency+']').parent();
		if(elementParent.checkbox('is checked')){
			uncheckDependency(dependency);
		}
		elementParent.checkbox('disable');
		
		
		
	}
	
});