function calc_word2vec() {
    if(typeof ga === 'function') {
        ga('send', 'event', 'ABT', 'click', 'AB Test Tool Calc Stats');
    }
    $("#w2vSubmitButton").hide();
    $("#scrollNudge").hide();
    
    $("#w2vLoadingButton").show();
    $("#compPlaceholder").empty();
    $("#nMostSimPlaceholder1").empty();
    $("#nMostSimPlaceholder2").empty();
    // $("#statsPlaceholder").empty();
    vote: $("[name='vote']:checked").val()
    $.ajax({
        url : "calc_word2vec/", // the endpoint
        type : "POST", // http method
        data : { 
            term_1 : $('#term_1').val(),
            term_2 : $('#term_2').val(),
            corpus : $("[name='corpus']:checked").val(),
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $("#w2vLoadingButton").hide();
            $("#w2vSubmitButton").show();
            $("#scrollNudge").show();

            $('.error-label').remove();
            n_most_sim_1 = null;
            n_most_sim_2 = null;
            similarity = -1;
            distance = -1;
            term_1 = ""
            term_2 = ""
            topn = ""
            if(json['term1'] != null) {
                term_1 = json['term1'];
            }
            if(json['term2'] != null) {
                term_2 = json['term2'];
            }
            if(json['topn'] != null) {
                topn = json['topn'];
            }
            if(json['n_most_sim_1'] != null) {
                n_most_sim_1 = JSON.parse(json['n_most_sim_1'])["data"];
            }
            if(json['n_most_sim_2'] != null) {
                n_most_sim_2 = JSON.parse(json['n_most_sim_2'])["data"];
            }  
            if(json['similarity'] != null) {
                similarity = json['similarity'];
            } 
            if(json['distance'] != null) {
                distance = json['distance'];
            }
           
            var templateResult_Comparison = Sqrl.Render(compared_metrics_template, {
                term1: term_1,
                term2: term_2,
                distance: distance,
                similarity: similarity
            }); 
            $("#compPlaceholder").html(templateResult_Comparison);       

            if(n_most_sim_1 != null) {
                var templateResult = Sqrl.Render(n_most_sim_template, {
                    topn: topn,
                    term: term_1,
                    n_most_sim: n_most_sim_1
                });
                $("#nMostSimPlaceholder1").html(templateResult);                            
            }                       
            if(n_most_sim_2 != null) {
                var templateResult = Sqrl.Render(n_most_sim_template, {
                    topn: topn,
                    term: term_2,
                    n_most_sim: n_most_sim_2
                });
                $("#nMostSimPlaceholder2").html(templateResult);                            
            }                    
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $("#w2vLoadingButton").hide();
            $("#w2vSubmitButton").show();
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


function calc_stats() {
    if(typeof ga === 'function') {
        ga('send', 'event', 'ABT', 'click', 'AB Test Tool Calc Stats');
    }
    $("#abtSubmitButton").hide();
    $("#abtLoadingButton").show();
    $("#boxplotPlaceholder").empty();
    $("#histplotPlaceholder").empty();
    $("#pPlaceholder").empty();
    $("#statsPlaceholder").empty();
    $("#scrollNudge").hide();
    ttest_equal_var = false;
    if ($('#id_ttest_equal_var').is(":checked"))
    {
        ttest_equal_var = true;
    }
    $.ajax({
        url : "calc_stats/", // the endpoint
        type : "POST", // http method
        data : { 
            var_1_input : $('#var_1_input').val(),
            var_2_input : $('#var_2_input').val(),
            num_permutations : $('#num_permutations').val(),
            ttest_equal_var:  ttest_equal_var
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $("#abtLoadingButton").hide();
            $("#abtSubmitButton").show();
            $("#scrollNudge").show();
            $('.error-label').remove();
            // $('#post-text').val(''); // remove the value from the input
            $('#var_1_input').val(json['var_1']);
            $('#var_2_input').val(json['var_2']);
            var_1_summary = null;
            var_2_summary = null;
            if(json['var_1_summary'] != null) {
                var_1_summary = JSON.parse(json['var_1_summary']);
            }
            if(json['var_2_summary'] != null) {
                var_2_summary = JSON.parse(json['var_2_summary']);
            }  
            equal_var = 'No';
            if(json['equal_var'] != null) {
                if(json['equal_var'] == true){
                    equal_var = 'Yes';
                } 
            }         
            
            if(var_1_summary != null && var_2_summary != null) {
                var templateResult = Sqrl.Render(stat_template, {
                    statHeaders: var_1_summary["index"],
                    stat_var_1: var_1_summary["data"],
                    stat_var_2: var_2_summary["data"]
                });
                $("#statsPlaceholder").html(templateResult);                            
            }   
            if(json['hypo_p'] != null) {                
                var templateResult_P = Sqrl.Render(p_template, {
                    hypo_p: (json['hypo_p']).toFixed(5),
                    num_perm: json['num_perm'],
                    ttest_p: (json['ttest_p']).toFixed(5),
                    min_sample_size: (json['min_sample_size']).toFixed(0),
                    equal_var: equal_var,
                   // chi_sq_p: (json['chi_sq_p']).toFixed(5),
                }); 
                $("#pPlaceholder").html(templateResult_P);                     
            }
            if(json['boxplot_img'] != null && json['boxplot_img'] != "") {  
                var templateResultBoxplotImage = Sqrl.Render(boxplot_template, {
                    image_data_boxplot: json["boxplot_img"]
                });
                $("#boxplotPlaceholder").html(templateResultBoxplotImage);  
            }   

            if(json['hist_img'] != null && json['hist_img'] != "") {  
                var templateResultHistImage = Sqrl.Render(histplot_template, {
                    image_data_histplot: json["hist_img"]
                });
                $("#histplotPlaceholder").html(templateResultHistImage);  
            }  
            
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $("#abtLoadingButton").hide();
            $("#abtSubmitButton").show();
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


var compared_metrics_template = `
<div class="row">
    <h4 class="col">Comparison</h4>

</div>
<div class="row">
<p class="col"><b>{{term1}}</b> compared to <b>{{term2}}</b></p>
</div>
<div class="row">
    <div class="col">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col" class="w-75">Metric</th>
                    <th scope="col" class="w-25">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Distance</th>
                    <td>{{distance}}</td>
                </tr>
                <tr>
                    <td>Similarity</th>
                    <td>{{similarity}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
`
var n_most_sim_template = `
<div class="row">
    <h4 class="col">{{topn}} most similar</h4>
</div>
<div class="row">
<p class="col">Top <b>{{topn}}</b> tokens most similar to <b>{{term}}</b></p>
</div>
<div class="row">
    <div class="col">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">Token</th>
                    <th scope="col">Similarity</th>
                </tr>
            </thead>
            <tbody>
                {{each(options.n_most_sim)}}
                <tr>
                    {{js(options.word = options.n_most_sim[@index][0])/}}
                    {{js(options.similarity = options.n_most_sim[@index][1])/}}

                    <td>{{word}}</td>
                    <td>{{similarity}}</td>
                </tr>
                {{/each}}
            </tbody>
        </table>
    </div>
</div>
`


var histplot_template = `
<div class="row">
    <h4 class="col">Histograms</h4>
</div>
<div class="row">
    <div class="col">
        <img src="data:image/png;base64,{{image_data_histplot}}" class="img-fluid" />
    </div>
</div>
`

var boxplot_template = `
<div class="row">
    <h4 class="col">Boxplot & Swarmplot</h4>
</div>
<div class="row">
    <div class="col">
        <img src="data:image/png;base64,{{image_data_boxplot}}" class="img-fluid" />
    </div>
</div>
`

var p_template = `
<div class="row">
    <h4 class="col">p-values and minimum sample size</h4>
</div>
<div class="row">
    <div class="col">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col" class="w-75">Test</th>
                    <th scope="col" class="w-25">p-value</th>
                </tr>
            </thead>
            <tbody>

            <tr>
                <td>Bootstrapped hypothesis test with {{num_perm}} permutations</th>
                <td>p = {{hypo_p}}</td>
            </tr>
            <tr>
                <td>Welch T-Test, two-sided, independent samples; Equal variance: {{equal_var}}</th>
                <td>p = {{ttest_p}}</td>
            </tr>
            <tr>
                <td>Minimum sample size for &alpha; = 0.05, &beta; = 0.8</th>
                <td>n = {{min_sample_size}}</td>
            </tr>    
        </tbody>
    </div>
</div>
`

var stat_template = `
<div class="row">
    <h4 class="col">Summary Statistics</h4>
</div>
<div class="row">
    <div class="col">
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Control</th>
                    <th scope="col">Treatment</th>
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
    </div>
</div>        
`