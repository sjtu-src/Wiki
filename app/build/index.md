<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    /* 这里的CSS只影响当前页面 */
button {
  padding: 0.8em 1.8em;
  border: 2px solid #17C3B2;
  position: relative;
  overflow: hidden;
  background-color: transparent;
  text-align: center;
  text-transform: uppercase;
  font-size: 16px;
  transition: .3s;
  z-index: 1;
  font-family: inherit;
  color: #17C3B2;
  left: 50%;
  transform: translateX(-50%);
}

button::before {
  content: '';
  width: 0;
  height: 300%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(45deg);
  background: #17C3B2;
  transition: .5s ease;
  display: block;
  z-index: -1;
}

button:hover::before {
  width: 105%;
}

button:hover {
  color: #111;
}

.md-typeset a {

 color: #46ffe9fe;

 text-decoration: underline;

}
.container{
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  text-align: center;
  margin-top: 100px;
}

.container h1:nth-child(1) {
  color: #355c7d;
  font-family: 'Fira Code', monospace;
  font-weight: 800;
  font-size: 20px;
  margin: 0 0 0 35%;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  width: 170px;
  animation: type 2s steps(40,end) forwards;
}

.container h1:nth-child(2) {
  opacity: 0;
  font-family: "Work Sans", sans-serif;
  margin: 0 auto auto auto;
  background: linear-gradient(to right, #eea949, #ea9c1f, #ee7206);
  font-weight: 800;
  font-size: 100px;  
  width: 430px;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  overflow: hidden;
  animation: shring-animation 2.2s steps(40,end) 2s forwards, blink .5s step-end infinite alternate;
}

@keyframes shring-animation {
  0% {
    background-position: 0 0;
    opacity: 0;
    width: 0;
  }
  1% {
    background-position: 0 0;
    opacity: 1;
    border-right: 1px solid orange;
  }
  50% {
    background-position: 150px 0;
    opacity: 1;
    border-right: 1px solid orange;
  }
  100% {
    background-position: 400px 0;
    opacity: 1;
    border-right: 1px solid orange;
  }
}

@keyframes type {
  0% {
    width: 0;
  }
  1%, 99%{
    border-right: 1px solid orange;
  }
  100%{
    border-right: none;
  }
}

@keyframes blink {
  50% {
    border-color: transparent;
  }
}

  </style>
</head>
<body>
  <!-- 页面内容 -->
</body>

</html>
<div class = "container">
  <h1>Hi, my name is</h1>
  <h1>SRC</h1>
</div>


​																	<button>[explore](chapter_preface)</button>

