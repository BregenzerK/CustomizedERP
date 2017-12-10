$(document).ready(function(){

	$('.tabular.menu .item').tab();
	$('.ui.checkbox').checkbox();

	var counterProdukt=1;
	var counterGruppe=1;
	var counterKategorie =1;
	
	$('#addProduct').click(function(){
		var clone = $('#produkttyp_0').clone(true);
		
		clone.attr('id', 'produkttyp_'+counterProdukt);
		clone.find('input:checkbox, input:text').each(function(){
			var id = $(this).parent().attr("id");
			$(this).parent().attr("id",id+counterProdukt);
			$(this).attr('id', 'id_form-'+counterProdukt+'-'+id);
			$(this).attr('name', 'form-'+counterProdukt+'-'+id);
		});
		counterProdukt+= 1;
		$('#id_form-TOTAL_FORMS').val(counterProdukt);
		clone.find('input:text').val('');
		$(this).before(clone);
		$('.ui.checkbox').checkbox();
	});
	
	$('#plus_gruppen').click(function(){
		var groupname = $('#gruppe_0').find('input').val();
		var group = '<br><div class="ui input" id="gruppe_'+counterGruppe+'"> <input id="id_form-'+counterGruppe+'-name" maxlength="50" name="form-'+counterGruppe+'-name" type="text" value="'+groupname+'"></div><br>';
		counterGruppe+=1;
		$('#gruppe_0').parent().find('input:hidden:first').val(counterGruppe);
		$('#kundengruppen').append(group);
		$(this).parent().find("input").val('');
	});
	
	$('#plus_kategorie').click(function(){
		var kategoriename = $('#kategorie_0').find('input').val();
		var kategorie = '<br><div class="ui input" id="kategorie_'+counterKategorie+'"> <input id="id_form-'+counterKategorie+'-kategorie" maxlength="50" name="form-'+counterKategorie+'-kategorie" type="text" value="'+kategoriename+'"></div><br>';
		counterKategorie+=1;
		$('#kategorie_0').parent().find('input:hidden:first').val(counterKategorie);
		$('#produktkategorien').append(kategorie);
		$(this).parent().find("input").val('');
	});

});
