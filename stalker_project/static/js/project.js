/* Project specific Javascript goes here. */

            // Add active class to the current button (highlight it)
            var header = document.getElementById("navigation");
            var btns = header.getElementsByClassName("navlink");
            for (var i = 0; i < btns.length; i++) {
              btns[i].addEventListener("click", function() {
                  console.log('clicked')
              var current = document.getElementsByClassName("active");
              if (current.length > 0) { 
                current[0].className = current[0].className.replace(" active", "");
              }
              this.className += " active";
              });
            } 