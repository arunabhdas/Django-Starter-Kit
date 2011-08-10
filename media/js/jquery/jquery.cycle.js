(function($){
 $.fn.cycle = function() {
    var $slides = $(this).children();
    var slide_count = $slides.length;
    var current = 1;
    cycle = function(){
        if (current > slide_count){
            current = 1;
        }
        var next = current + 1;
        if (next > slide_count){
            next = 1;
        }
        $('#slide-'+current).animate({ opacity: 'hide'}, 1000, function(){
                $(this).css('z-index','5')
            });
        $('#slide-'+next).animate({ opacity: 'show', 'filter': ''}, 900, function(){
                $(this).css('z-index','6')
                if(jQuery.browser.msie)
                    $(this).get(0).style.removeAttribute('filter');
            })
        $('#counter-'+current).removeClass('active')
        $('#counter-'+next).addClass('active')
        current ++;
    }
    function clearTypeFix($slides) {
        function hex(s) {
            s = parseInt(s).toString(16);
            return s.length < 2 ? '0'+s : s;
        };
        function getBg(e) {
            for ( ; e && e.nodeName.toLowerCase() != 'html'; e = e.parentNode) {
                var v = $.css(e,'background-color');
                if (v.indexOf('rgb') >= 0 ) {
                    var rgb = v.match(/\d+/g);
                    return '#'+ hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
                }
                if (v && v != 'transparent')
                    return v;
            }
            return '#ffffff';
        };
        $slides.each(function() { $(this).css('background-color', getBg(this)); });

    };
    return this.each(function() {

        var counter = slide_count;
        html= '';
        for (var i = 1; i <= counter; i++){
            if (i == 1)
                _class = ' active'
            else _class = '';
            html += '<div id=\'counter-'+i+'\' class=\'circle'+_class+'\'></div>';
        }
        $('#counter-slideshow').append(html);
        if(jQuery.browser.msie)
            clearTypeFix($slides);
        setInterval( "cycle()", 7000 );
    });
 };
})(jQuery);
