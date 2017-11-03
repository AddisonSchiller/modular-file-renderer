
<!-- <script src="/static/js/jquery-1.11.3.min.js"></script> -->
<script src="${base}/js/Magnifier.js"></script>
<script src="${base}/js/Event.js"></script>
<link rel="stylesheet" href="${base}/css/Magnifier.css">

<img id="thumb" src="${url}">
<div class="magnifier-preview" id="preview" style="width: 200px; height: 200px"></div>

<script type="text/javascript">
var evt = new Event(),
    m = new Magnifier(evt);
m.attach({
    thumb: '#thumb',
    large: '${url}',
    largeWrapper: 'preview',
    zoom: 6
});
</script>


<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
