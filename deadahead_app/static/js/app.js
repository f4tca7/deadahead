function calc_stats() {
    console.log("post_calc is working!") // sanity check
    $("#statsPlaceholder").empty();
    $.ajax({
        url : "calc_stats/", // the endpoint
        type : "POST", // http method
        data : { 
            var_1_input : $('#var_1_input').val(),
            var_2_input : $('#var_2_input').val(),
            num_permutations : $('#num_permutations').val(),
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('.error-label').remove();
            // $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            $('#var_1_input').val(json['var_1']);
            $('#var_2_input').val(json['var_2']);
            var_1_summary = null;
            var_2_summary = null;
            if(json['var_1_summary'] != null) {
                var_1_summary = JSON.parse(json['var_1_summary']);
            }
            if(json['var_1_summary'] != null) {
                var_2_summary = JSON.parse(json['var_2_summary']);
            }         
            if(var_1_summary != null && var_2_summary != null) {
                var templateResult = Sqrl.Render(stat_template, {
                    statHeaders: var_1_summary["index"],
                    stat_var_1: var_1_summary["data"],
                    stat_var_2: var_2_summary["data"]
                });
                $("#statsPlaceholder").html(templateResult)
                            
            }   
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('.error-label').remove();
            var tmpData = JSON.parse(xhr.responseText);
            var formattedJson = JSON.stringify(tmpData, null, '\t');
            console.log(tmpData);
            for(var index in tmpData) {                
                if($("#" + index).length != 0) {
                    console.log(index + " : " + tmpData[index] + 'bb');
                    $("#" + index).after('<small class="error-label red-color">' + tmpData[index] + '</small>');
                }
            }
        }
    });
};

// Submit post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    post_calc();
});

$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

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

});

var stat_template = `
<table class="table">
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Variant 1</th>
            <th scope="col">Variant 2</th>
        </tr>
    </thead>
    <tbody>
        {{each(options.statHeaders)}}
        <tr>
            {{js(options.val_1 = options.stat_var_1[@index])/}}
            {{js(options.val_2 = options.stat_var_2[@index])/}}

            <th scope="row">{{@this}}</th>
            <td>{{val_1}}</td>
            <td>{{val_2}}</td>
        </tr>
        {{/each}}
    </tbody>
</table>       
    
`

// var templateResult = Sqrl.Render(myTemplate, {
//     fav: "Squirrelly", cake: "Chocolate"
// })

// console.log(templateResult)

// {{each(stat_headers)}}
// {{@this}}
// {{/each}}

// {{each(stat_var_1)}}
// {{@this}}
// {{/each}} 

// {{each(stat_var_2)}}
// {{@this}}
// {{/each}}