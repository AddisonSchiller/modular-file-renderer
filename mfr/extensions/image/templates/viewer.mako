 <img style="max-width: 800; max-height: 800;" src="${url}">   

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

<!-- <script src="/static/js/jquery-1.11.3.min.js"></script> -->
<script src="${base}/js/intense.min.js"></script>

<script>
window.onload = function() {
    // Intensify all images on the page.
    var element = document.querySelector( 'img' );
    Intense( element );
}
</script>