$(document).ready(function() {
    // Retrieve the CSRF token from the cookie
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!settings.crossDomain && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
      }
    }
  });

$(document).ready(function() {
    $('#online-toggle').on('click', function() {
      var currentState = $(this).attr('data-state');
      
      $.ajax({
        type: 'POST',
        url: 'update_state/',  
        data: {
          state: currentState
        },
        success: function(response) {
          // Update button text and state based on the response
          if (response.state === true) {
            $('#online-toggle').text('Online');
            $('#online-toggle').attr('data-state', 'online');
            $('#online-toggle').attr('class', 'btn btn-outline-success');
          } else {
            $('#online-toggle').text('Offline');
            $('#online-toggle').attr('data-state', 'offline');
            $('#online-toggle').attr('class', 'btn btn-danger');
          }
        },
        error: function(xhr, status, error) {
          // Handle error if the AJAX request fails
          console.log(error);
        }
      });
    });
  });
});