/**
 * Created by alan on 1/12/17.
 */

var recommendAnimate = function () {
    var recommend = $('[data-section="recommend"]');
    if (recommend.length > 0) {
        recommend.waypoint(function (direction) {
            if (direction === 'down' && !$(this.element).hasClass('animated')) {
                setTimeout(function () {
                    recommend.find('.to-animate').each(function (k) {
                        var el = $(this);
                        setTimeout(function () {
                            el.addClass('fadeInUp animated');
                        }, k * 200, 'easeInOutExpo');
                    });
                }, 200);
                $(this.element).addClass('animated');
            }
        }, {offset: '80%'});
    }
};

$('#add-author').click(function() {
  // get the last DIV which ID starts with ^= "klon"
  var $div = $('div[id^="author_"]:last');
  // Read the Number from that DIV's ID (i.e: 3 from "klon3")
  // And increment that number by 1
  var num = parseInt($div.prop("id").match(/\d+/g), 10) + 1;
  // Clone it and assign the new ID (i.e: from num 4 to ID "klon4")
  var $klon = $div.clone().prop('id', 'author_' + num);
  // Finally insert $klon wherever you want
  $div.after($klon);
  $('input[name^="author_firstname_"]:last').prop('name', 'author_firstname_' + num);
  $('input[name^="author_lastname_"]:last').prop('name', 'author_firstname_' + num);
  $('input[name^="author_email_"]:last').prop('name', 'author_firstname_' + num);
  $('input[name^="author_organization_"]:last').prop('name', 'author_firstname_' + num);
  $('h3[id^="author_label_"]:last').text('Author #' + num);
});


function post_paper_meta() {
  checkProcess(taggle.getTagValues().toString(), "/api/get_result/meta/", $('#paper').serialize())
}

function checkProcess(payload, url, data) {
    jQuery.ajax({
        url: url + payload,
        data: data,
        success: function (result) {
            var response = JSON.parse(JSON.stringify(result));
            $("#please-wait").hide();
            $("#upload-message").show();
            if (response["status"] === "Success") {
                $("#result-start").html(response["payload"]);
                $('.initial').initial({charCount: 2, fontSize: 40});
                $(window).trigger('resize');
                $('html, body').animate({
                    scrollTop: $('[data-section="recommend"]').offset().top - 100
                }, 500);
                recommendAnimate();
                Dropzone.instances[0].removeAllFiles();
                $("#result-start").removeClass();
                $("#nav-recommendation").show();
            } else if (response["status"] === "TooMany") {
                Dropzone.instances[0].removeAllFiles();
                $("#result-start").removeClass();
                // TODO: add error alert
                $("#result-start").html(response["payload"]);
                $('.initial').initial({charCount: 2, fontSize: 40});
                $(window).trigger('resize');
                $('html, body').animate({
                    scrollTop: $('[data-section="recommend"]').offset().top - 100
                }, 500);
                recommendAnimate();
                Dropzone.instances[0].removeAllFiles();
                $("#result-start").removeClass();
                $("#nav-recommendation").show();
                swal({
                    title: "Oops",
                    text: response["message"],
                    type: "warning",
                    showCancelButton: true,
                    // confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Cool!",
                    closeOnConfirm: true
                }, function () {
                    setTimeout(function () {
                        $('html, body').animate({
                            scrollTop: $('.manual-keyword-input').offset().top - 100
                        }, 500);
                    }, 500, 'easeInOutExpo');
                });
            } else if (response["status"] === "Error") {
                Dropzone.instances[0].removeAllFiles();
                $("#result-start").removeClass();
                // TODO: add error alert
                swal({
                    title: "Oops",
                    text: response["message"],
                    type: "warning",
                    showCancelButton: true,
                    // confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Cool!",
                    closeOnConfirm: true
                }, function () {
                    setTimeout(function () {
                        $('html, body').animate({
                            scrollTop: $('.manual-keyword-input').offset().top - 100
                        }, 500);
                    }, 500, 'easeInOutExpo');
                });
                // swal("Oops", response["payload"], "error");
            } else if (response["status"] === "Processing") {
                checkProcess(payload, url)
            }
            // TODO: make previous result accessable instead of clearing the dropbox.

        },
        async: true
    });
}

