$(document).ready(function () {

	let pullData;
	let tabindex = 0;

	$("#search_form").submit(function (event) {
		event.preventDefault(); //prevent default action 
		clearInterval(pullData);
		$('.loading-section.data').removeClass('hide');
		$('.crawl-section').addClass('loading');

		let post_url = $(this).attr("action"); //get form action url
		let request_method = $(this).attr("method"); //get form GET/POST method
		let form_data = $(this).serialize(); //Encode form elements for submission
		let thread_status = '';
		let client_key = '';
		let tbody_data = [];
		$('.crawl-section .table-div #crawl_result_table tbody').html('');

		pullData = setInterval(
			function () {
				var page = parseInt($('#crawl_result_table_wrapper ul.pagination li.active a').html())-1;
					$.ajax({
						url: post_url,
						type: request_method,
						data: form_data + "&thread_status=" + thread_status + "&client_key=" + client_key,
					}).done(function (result) { //
						console.log(page);
						response = JSON.parse(result);
						response_data = response[0];
						thread_status = response[1];
						client_key = response[2];

						if (response_data.length > 0) {
							for (let i = 0; i < response_data.length; i++) {
								button_td = '<button class="btn btn-info claim-btn claim" data-lname="' + form_data['l_name_search'] + '">Claim</button>';
								response_data[i].unshift(button_td);
								tr_data = response_data[i];
								tbody_data.push(tr_data);
							}
						}

						if (thread_status == 'end') {
							clearInterval(pullData);
							$('.loading-section.data').addClass('hide');
							$('.crawl-section').removeClass('loading');
							$('.crawl-section .table-div').removeClass('hide');
							$('#crawl_result_table').DataTable();
						} else if (thread_status == 'crawling') {
							if (tbody_data.length > 0) {

								$('.loading-section.data').addClass('hide');
								$('.crawl-section').removeClass('loading');
								$('.crawl-section .table-div').removeClass('hide');
								$(".main-container").addClass('show_data');
								// tabindex = $('#crawl_result_table_wrapper ul.pagination li.active a').data('dt-idx');
								if ($.fn.dataTable.isDataTable('#crawl_result_table')) {
									var table = $('#crawl_result_table').DataTable();
									table.destroy();
									$('#crawl_result_table').empty();
									$('#crawl_result_table').DataTable({
										data: tbody_data,
										columns: [
											{ title: "" },
											{ title: "Name" },
											{ title: "Held In", className: 'heldin-td' },
											{ title: "Last Address", className: 'last-address-td' },
											{ title: "Property ID", className: 'property-id-td' },
											{ title: "Reported By", className: 'reported-by-td' },
											{ title: "Amount", className: 'amount-td' }
										]
									});
									$('#crawl_result_table').DataTable().page(page).draw('page');
								} else {
									$('#crawl_result_table').DataTable({
										data: tbody_data,
										columns: [
											{ title: ""},
											{ title: "Name" },
											{ title: "Held In", className: 'heldin-td' },
											{ title: "Last Address", className: 'last-address-td' },
											{ title: "Property ID", className: 'property-id-td' },
											{ title: "Reported By", className: 'reported-by-td' },
											{ title: "Amount", className: 'amount-td' }
										]
									});
								}

							}
						}
					})
			}
			, 5000);

	});

	$('#crawl_result_table').on('click', 'tbody .claim', function () {
		document.getElementById("claim_people_form").reset();
		$('#claimModal #claim_sumbit_btn').attr('disabled', 'true');

		$('#l_name_modal').val($('#l_name_search').val());
		$('#heldin_modal').val($(this).parent().parent().children('.heldin-td').text())
		$('#last_address_modal').val($(this).parent().parent().children('.last-address-td').text())
		$('#property_id_modal').val($(this).parent().parent().children('.property-id-td').text())
		$('#reported_by_modal').val($(this).parent().parent().children('.reported-by-td').text())
		$('#amount_modal').val($(this).parent().parent().children('.amount-td').text())
		$('#claimModal').modal();
		
	});

	$('.table-div').on('click', '#crawl_result_table_wrapper ul.pagination li.page-item a', function() {
		
		tabindex = parseInt($(this).html()) - 1;
	})

	$('#claimModal #customCheck').change(function () {
		if ($('#claimModal #claim_sumbit_btn').attr('disabled')) {
			$('#claimModal #claim_sumbit_btn').removeAttr('disabled');
		} else {
			$('#claimModal #claim_sumbit_btn').attr('disabled', 'true');
		}
	});

	$("#claim_people_form").submit(function (event) {
		event.preventDefault(); //prevent default action 
		$('#claimModal #claim_sumbit_btn').attr('disabled', 'true');

		$('.loading-section.mail').removeClass('hide');
		$('.crawl-section').addClass('loading');

		let post_url = $(this).attr("action"); //get form action url
		let request_method = $(this).attr("method"); //get form GET/POST method
		let form_data = $(this).serialize(); //Encode form elements for submission

		$.ajax({
			url: post_url,
			type: request_method,
			data: form_data
		}).done(function (response) { //
			$('#claimModal').modal('hide');
			swal("SUCCESS!", "The people data saved successfully!", "success");

			$('.loading-section.mail').addClass('hide');
			$('.crawl-section').removeClass('loading');
		});

	});
	$(".pannel_button").click(function () { 
		
		if($(".search-div-wrapper").hasClass("active")){
			$(".search-div-wrapper").removeClass('active');
			$(".dark_bg").addClass('hide');
		}else{
			$(".search-div-wrapper").addClass('active');
			$(".dark_bg").removeClass('hide');
		}

	});
	$('.dark_bg').click(function () { 
		$(".search-div-wrapper").removeClass('active');
		$(".dark_bg").addClass('hide');
	 })
});

