$(document).ready(function() {
	  
	  $('.ui.checkbox').checkbox();
	  $('.ui.sidebar')
  		.sidebar('show');
  	
  	$('.ui.pointing.label').css("display","inline");

    $('.ui.dropdown')
      .dropdown({
        on: 'hover',
      })
    ;
    
	calc_messages_number();

	$('#overview tbody tr').click( function() {
    	window.location = $(this).attr('href');
		}).hover( function() {
    		$(this).toggleClass('hover');
			});
	
	function grab_selected() {
		var products= [];
		$('#overview').find('input[type="checkbox"]:checked').each(function () {
		        products.push($(this).attr('id'));
		});
		return products;
	}
	
	/*$('#inventurliste').click(function(){
 		var products = grab_selected();
       	url = '/lager/inventurliste';
       	var i=0;
       	for (i = 0; i < products.length; ++i) {
       		url+= '/'+products[i];
       	}
       	window.location.href=url;
     }); */
       
	var counter = 1;
	$('#addPosition').click(function(){
		var clone = $('#0').clone(true);
		clone.attr('id', counter);
		clone.find('input, select').each(function(){
			$(this).val('');
			var id = $(this).attr('id').replace(/\d+/g, counter);
			$(this).attr('id', id);
			var name = $(this).attr('name').replace(/\d+/g, counter);
			$(this).attr('name', name);
		});
		counter+=1;
		$('#positions tbody').find('input:hidden:first').val(counter);
		clone.insertBefore($('#positions').find('tr:last'));
	});
	
	//Bestellung ohne BANF
	$('#lieferanten').dropdown({
	    onChange: function (value, lieferant) {
	        get_Produkte(lieferant);
	        $('#id_summe').val('');
	    }
	});
	
	function get_Produkte(lieferant){
		var selects = $(document).find('[name*=produkt_bestellung]');
		$.ajax({
			url: "/Produkte", //give your URL here
			typ: "GET",
			data: {'lieferant':lieferant} , 
			contentType: "application/json;charset=utf-8",
			dataType: "json",
			success: function(data){
				var options = data;
				$.each(selects, function (i, item){
					var el = $(document).find('#'+selects[i].id);
					el.empty();
					el.append($("<option></option>").text('---------'));
					$.each(options, function(value,key) {
						el.append($("<option></option>")
							     .attr("value", value).text(key));
					});
				});
			}
		}); 
	}
	
	$(document).find('[name*=produkt_bestellung]').change(function(){
		var fabrikat = 	$(this).val();
		var id = $(this).parent().parent().attr('id');
		$.ajax({
  			url: "/Preis", //give your URL here
  			typ: "GET",
  			data: {'fabrikat':fabrikat} , 
  			contentType: "application/json;charset=utf-8",
            dataType: "json",
  			success: function(data){
    			$('#id_form-'+id+'-einkaufspreis_bestellung').val(data.fields.EK);
    			var menge = $('#id_form-'+id+'-anzahl_bestellung');
    			menge.val(1.0);
    			calc_sum_bestellung_ohne_banf(id);
  			}
		}); 
	});
	
	function calc_sum_bestellung_ohne_banf(id){
		var summe = 0;
		var preis = $('#id_form-'+id+'-einkaufspreis_bestellung').val();
		preis = preis.replace(',', '.');
		preis = parseFloat(preis);
		
		var menge = parseFloat($('#id_form-'+id+'-anzahl_bestellung').val().replace(',','.'));
		summe = preis*menge;
		$('#id_form-'+id+'-summe_bestellung').val(summe);
		var positions=0;
		$(document).find('[name*=-summe_bestellung').each(function(){
			positions+= parseFloat($(this).val());
		});
		$('#id_summe').val(positions);
		
	}
	$(document).find('[name*=anzahl_bestellung]').change(function(){
		
	})
	
	//create Kauf/ Angebot
	var bestand=0;
	
	$(document).find('[name*=produkt_kauf]').change(function(){
		var fabrikat = 	$(this).val();
		var id = $(this).parent().parent().attr('id');
		$.ajax({
  			url: "/Preis", //give your URL here
  			typ: "GET",
  			data: {'fabrikat':fabrikat} , 
  			contentType: "application/json;charset=utf-8",
            dataType: "json",
  			success: function(data){    		
    			$('#id_form-'+id+'-einzelpreis').val(data.fields.verkaufspreis);
    			var menge = $('#id_form-'+id+'-menge');
    			menge.val(1.0);
    			bestand=data.fields.lagerbestand;
    			calc_sum(id);
    			check_availability(menge.val(), id)
  			}
		}); 
	});
	
	$(document).find('[name*=-menge]').change(function(){
		if ($(this).val()<=0){
			$(this).val(1);
		}
		var id = $(this).parent().parent().attr('id');
		calc_sum(id);
		check_availability($(this).val(), id);
		
	});
	
	$('#id_rabatt').change(function(){
		calc_total();
	});
	
	$('#id_rabattarten').change(function(){
		calc_total();
	});
	
	function check_availability(menge, id){
		if (menge <= bestand){
			
			$('#'+id+' td i.green.checkmark.icon').css({'display':'inline'});
			$('#'+id+' td i.red.remove.icon').css({'display':'none'});
		}
		else{
			$('#'+id+' td i.green.checkmark.icon').css({'display':'none'});
			$('#'+id+' td i.red.remove.icon').css({'display':'inline'});
		}
	}
	
	function calc_sum(id){
		var summe = 0;
		var einzelpreis = $('#id_form-'+id+'-einzelpreis').val();
		einzelpreis = einzelpreis.replace(',', '.');
		einzelpreis = parseFloat(einzelpreis);
		
		var menge = parseFloat($('#id_form-'+id+'-menge').val().replace(',','.'));
		summe = einzelpreis*menge;
		$('#id_form-'+id+'-summe').val(summe);
		calc_total();
		
	}
	
	function calc_total(){
		var positions_total=0;
		$(document).find('[name*=-summe]').each(function(){
			positions_total = positions_total + parseFloat($(this).val());
		});
		$('#zwischensumme').val(positions_total);
		var gesamt =positions_total;
		var rabatt = $('#id_rabatt').val();
		var rabattart = $('#id_rabattarten').val()
		if (rabattart=="betragsrabatt"){
			gesamt = positions_total-rabatt;
		}else if(rabattart=="prozentrabatt"){
			rabatt = (100-rabatt)/100;
			gesamt=positions_total*rabatt;
			gesamt = gesamt.toFixed(2);
		}
		$('#id_summe').val(gesamt);

	}
	
	//create Bestellung
	$(document).find('[name*=anzahl]').change(function(){
		if ($(this).val()<=0){
			$(this).val(1);
		}
		var id = $(this).parent().parent().attr('id');
		
		if ($(this).attr('name') == 'form-'+id+'-anzahl'){
			calc_sum_bestellung(id);
		}
		else if ($(this).attr('name') == 'form-'+id+'-anzahl_bestellung'){
			calc_sum_bestellung_ohne_banf(id);
		}
		
	});
	
	$(document).find('[name*=einkaufspreis]').change(function(){
		var id = $(this).parent().parent().attr('id');
		if ($(this).attr('name') == 'form-'+id+'-einkaufspreis'){
			calc_sum_bestellung(id);
		}
		else if ($(this).attr('name') == 'form-'+id+'-einkaufspreis_bestellung'){
			calc_sum_bestellung_ohne_banf(id);
		}
	});
	
	function calc_sum_bestellung(id){
		var summe = 0;
		var einkaufspreis = $('#id_form-'+id+'-einkaufspreis').val();
		einkaufspreis = einkaufspreis.replace(',', '.');
		einkaufspreis = parseFloat(einkaufspreis);
		
		var menge = parseFloat($('#id_form-'+id+'-anzahl').val().replace(',','.'));
		summe = einkaufspreis*menge;
		$('#id_form-'+id+'-summe').val(summe);

		total=0;
		$(document).find('[name*=-summe]').each(function(){
			total+= parseFloat($(this).val())
		});
		$('#id_summe').val(total);
		
	}
	
	//Inventurliste
	$(document).find('[name*=lagerbestand_real]').change(function(){
		if ($(this).val()<=0){
			$(this).val(1);
		}
		var id = $(this).parent().parent().attr('id');
		calc_sum_inventur(id);
	});
	
	$(document).find('[name*=EK]').change(function(){
		var id = $(this).parent().parent().attr('id');
		calc_sum_inventur(id);
	});
	
	function calc_sum_inventur(id){
		var summe = 0;
		var einkaufspreis = $('#id_form-'+id+'-EK').val();
		einkaufspreis = einkaufspreis.replace(',', '.');
		einkaufspreis = parseFloat(einkaufspreis);
		
		var menge = parseFloat($('#id_form-'+id+'-lagerbestand_real').val().replace(',','.'));
		summe = einkaufspreis*menge;
		$('#id_form-'+id+'-gesamtwert').val(summe);
		
	}
	
	function calc_messages_number(){
		$.ajax({
  			url: "/Messages",
  			typ: "GET",
  			success: function(data){    		
  				$('#messages_number').text(data);
  			},
		}); 
		
	}
	
	//Bestellung Details (Wareneingang)
	$('#complete').change(function(){
		var state = $(this).prop('checked');
		$(document).find('[name*=erhalten]').each(function(){
			if (state==true){
				$(this).attr('checked', 'checked');
			}else{
				$(this).removeAttr('checked');
			}
			
		})
	});
	$(document).find('[name*=erhalten]').change(function(){
		var state = $(this).prop('checked');
		if (state==false){
			$('#complete').removeAttr('checked');
		}
	});

	//Banf Details
	var bestellsumme = parseFloat($('#bestellsumme').text().replace(',', '.'));
	function calc_bestellsumme(){
		var summe = 0;
		summe = (parseFloat($('#id_einkaufspreis_banf').val().replace(',', '.'))*parseFloat($('#id_menge').val().replace(',', '.')));
		$('#id_summe_banf').val(summe);
		summe+= bestellsumme;
		$('#bestellsumme').text(summe);
	}
	
	$(document).find('[name*=banf]').change(function(){
		calc_bestellsumme()
	});
	$('#id_menge').change(function(){
		calc_bestellsumme();
	});
	
	  var csrftoken = $.cookie('csrftoken');
	    
	    function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		function sameOrigin(url) {
	    // test that a given url is a same-origin URL
	    // url could be relative or scheme relative or absolute
	    var host = document.location.host; // host + port
	    var protocol = document.location.protocol;
	    var sr_origin = '//' + host;
	    var origin = protocol + sr_origin;
	    // Allow absolute or scheme relative URLs to same origin
	    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	        // or any other URL that isn't scheme relative or absolute i.e relative.
	        !(/^(\/\/|http:|https:).*/.test(url));
		}
		$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
	            // Send the token to same-origin, relative URLs only.
	            // Send the token only if the method warrants CSRF protection
	            // Using the CSRFToken value acquired earlier
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    	}
		});
	

  })
;
