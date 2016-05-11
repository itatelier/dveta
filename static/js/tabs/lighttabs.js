(function($){				
	jQuery.fn.lightTabs = function(options){

		var createTabs = function(){
			var tabs = this;
			var i = 0;
			var $active_tab_hidden_param = $('input[name="active_tab"]');
			var active_tab = $active_tab_hidden_param.val();
			if (active_tab === 'None') {
				active_tab = 0;
			}

			showPage = function(i){
				$(tabs).children("div").children("div").hide();
				$(tabs).children("div").children("div").eq(i).show();
				$(tabs).children("ul").children("li").removeClass("active");
				$(tabs).children("ul").children("li").eq(i).addClass("active");
				$active_tab_hidden_param.val(i)
			};
								
			showPage(active_tab);
			
			$(tabs).children("ul").children("li").each(function(index, element){
				$(element).attr("data-page", i);
				i++;                        
			});
			
			$(tabs).children("ul").children("li").click(function(){
				showPage(parseInt($(this).attr("data-page")));
			});				
		};		
		return this.each(createTabs);
	};	
})(jQuery);