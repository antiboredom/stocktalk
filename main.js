// var $ = require('jquery');
var reqwest = require('reqwest');
var React = require('react');
var ReactDOM = require('react-dom');

var Stock = React.createClass({
	getInitialState: function() {
    var data = [
      {line: "", word: ""},
      {line: "", word: ""},
      {line: "", word: ""}
    ];

    return {data: data};
  },

	handleSubmit: function(e) {
  	e.preventDefault();
    document.querySelector('#welcome').style.display = 'none';
    var img = 'static/images/hold' + Math.ceil(Math.random()*2) + '.gif';
    this.setState({status: img});
    this.createVideo();
  },

  handleLineChange: function(i, e) {
  	var state = this.state.data.concat();
    state[i].line = e.target.value;
    this.setState({data: state});

    this.getKeyword(e.target.value, i);
  },

  getKeyword: function(text, i) {
    var self = this;
    reqwest({
      url: '/keyword',
      data: {text: text},
      success: function(data) {
        var state = self.state.data.concat();
        state[i].word = data.keywords[0];
        self.setState({data: state});
      }
    });
  },


  createVideo: function() {
    var self = this;

    var words = this.state.data.map(function(o) {
      return o.word;
    });

    var lines = this.state.data.map(function(o) {
      return o.line;
    });

    reqwest({
      url: '/create',
      method: 'post',
      data: {'word': words, 'text': lines, filetype: this.refs.filetype.value},
      success: function(data) {
        self.setState({downloadURL: data.url, status: null});
      },
      error: function() {
        self.setState({downloadUrl: null, status: null});
      }
    });

  },

  handleWordChange: function(i, e) {
   	var data = this.state.data;
    data[i].word = e.target.value;
    this.setState({data: data});
  },

  render: function() {
  	var self = this;
  	var phrases = this.state.data.map(function(item, i){
    	return (
      	<Phrase
        	word={item.word}
          placeholder={"Line " + (i+1)}
          line={item.line}
          key={i}
          tabIndex={i+1}
          handleLineChange={self.handleLineChange.bind(self, i)}
          handleWordChange={self.handleWordChange.bind(self, i)}
      	/>
    	);
    });

    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <div>{phrases}</div>
          {this.state.status ? '' :
            <div id="submitter">
              <select defaultValue="gif" ref="filetype">
                <option value="gif">GIF</option>
                <option value="mp4">VIDEO</option>
              </select>
              <input type="submit" value="Generate"/>
            </div>
          }
        </form>
        {this.state.status ? <Status status={this.state.status} /> : ''}
        {this.state.downloadURL && !this.state.status ? <Output src={this.state.downloadURL} /> : ''}
      </div>
    );
  }
});

var Status = React.createClass({
	render: function() {
  	return <div><img id="status" src={this.props.status} /></div>;
  }
});

var Output = React.createClass({
	render: function() {
  	var el;
    if (this.props.src.indexOf('.gif') > -1) {
    	el = <img id="out-img" src={this.props.src} />;
    } else {
    	el = <video loop="1" id="out-vid" controls="controls" src={this.props.src}></video>;
    }

    return (
      <div>
        {el}
        <a href={this.props.src} download>Download</a>
      </div>
    );
  }
});

var Phrase = React.createClass({
  clickWord: function(e) {
  	e.target.select();
  },

  render: function() {
    return (
    	<div className="line">
      	<input
        	type="text"
          value={this.props.line}
          tabIndex={this.props.tabIndex}
          placeholder={this.props.placeholder}
          onChange={this.props.handleLineChange}
          className="text"
        />

        <input
        	type="text"
          value={this.props.word}
          placeholder="Key word"
          onChange={this.props.handleWordChange}
          disabled={this.props.line.trim() === ''}
          onClick={this.clickWord}
          className="word"
        />
      </div>
    );
  }


});

ReactDOM.render(<Stock />, document.getElementById('container'));
