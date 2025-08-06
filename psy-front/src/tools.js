export function checkFill (t, arr) {
	if (t.check && (arr.some(ans => ans === null) || arr.some(ans => ans === ""))) {
		if (typeof t.showError === "function") {
			t.showError("请完成所有题目后再提交");
		} else {
			alert("请完成所有题目后再提交");
		}
		return false;
	}
	return true
}

export function step (t){
	t.step++;
	t.$nextTick(() => {
		window.scrollTo({ top: 0, behavior: "smooth" });
	});
}

export function checkFillStep (t, arr) {
	if (checkFill(t, arr)){
		step(t)
	}
}

class WebSocketService {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.listeners = [];
    this.messageQueue = [];
    this.connecting = false;
  }

  connect() {
    if (this.ws || this.connecting) return;
    this.connecting = true;
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => {
      console.log("ws连接成功");
      this.connecting = false;
      // 连接建立后，发送队列中的所有消息
      while (this.messageQueue.length > 0) {
        const msg = this.messageQueue.shift();
        console.log('send:', msg)
        this.ws.send(msg);
      }
    };
    this.ws.onmessage = (evt) => {
      const response = JSON.parse(evt.data);
      console.log('receive JSON data:', response)
      this.listeners.forEach(fn => fn(response));
    };
    this.ws.onclose = () => { 
      this.ws = null; 
      this.connecting = false;
    };
    this.ws.onerror = (e) => { 
      console.error('WebSocket error', e); 
      this.connecting = false;
    };
  }

  send(msg) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.log('send:', msg)
      this.ws.send(msg);
    } else {
      // 如果未连接，则放入队列
      this.messageQueue.push(msg);
    }
  }

  addMessageListener(fn) {
    this.listeners.push(fn);
  }

  removeMessageListener(fn) {
    this.listeners = this.listeners.filter(f => f !== fn);
  }
}

import config from './config.js'
console.log(config.wsUrl)
const wsInstance = new WebSocketService(config.wsUrl);
export default wsInstance;
