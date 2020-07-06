$(document).ready(function(){
	/*  Выпадающее меню и иконка  */
	$('.hamburger').on('click', function(e){
		e.preventDefault();
		$(this).toggleClass('opned');
		$('header nav').toggleClass('active');
		
	});
});