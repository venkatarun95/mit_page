const svgns = "http://www.w3.org/2000/svg";
const height = 600;
const width = 1000;
const pkt_width = 10;
const frame_interval = 32;
const bdp = 8;
const snd_y = height / 8;
const return_y = 3 * height / 8;
const snd_x = 100;
const traversal_time = 1000;
const buf_end = width - 5 * pkt_width;
const buf_start = buf_end - 2 * bdp * pkt_width;
const vel = (buf_start - snd_x) * frame_interval / traversal_time
const link_intersend = frame_interval * 10;

const graph_0 = [50, height * 0.9];
const graph_size = [width * 0.8, height * 0.4];
const max_time = 50;

// Keep track of what time it should be (independent of scheduling errors)
let cur_time = 0;
// So we can assign a unique id to each packet
let pkt_id = 0;
// Whether or not we are currently paused
let paused = true;
// Whether or not we are currently stopped
let stopped = false;

let cur_cwnd = 4 * bdp;
let cur_inflight = 4 * bdp;

// Times (in number of intersend times) at which packets should arrive at the buffer
const pkt_times = [0.1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
		   15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8,
		   32, 32.1, 32.2, 32.3, 32.4, 32.5, 32.6, 32.7
		  ];

const pause_times = [1, 14, 31, 42.3];

class Packet {
    constructor(x, y) {
	this.x = x;
	this.y = y;
	this.id = pkt_id;
	pkt_id += 1;
	const e = document.createElementNS(svgns, "rect");
	e.setAttributeNS(null, "width", pkt_width);
	e.setAttributeNS(null, "height", 20);
	e.setAttributeNS(null, "x", x);
	e.setAttributeNS(null, "y", y);
	e.setAttributeNS(null, "id", "pkt_" + this.id);
	if (this.id == 2 * bdp + 3 || this.id == 5 * bdp + 2) {
	    e.setAttributeNS(null, "style", "fill:rgb(255,0,0);stroke-width:1;stroke:rgb(0,0,0)");
	}
	else if (this.id % 2) {
	    e.setAttributeNS(null, "style", "fill:rgb(128,128,0);stroke-width:1;stroke:rgb(0,0,0)");
	}
	else {
	    e.setAttributeNS(null, "style", "fill:rgb(192,192,0);stroke-width:1;stroke:rgb(0,0,0)");
	}

	const svg = document.getElementById("svg_area");
	svg.appendChild(e);
    }

    redraw() {
	let e = document.getElementById("pkt_" + this.id);
	if (this.x > snd_x) {
	    e.setAttributeNS(null, "x", this.x);
	}
	else {
	    e.setAttributeNS(null, "x", -10);
	}
	e.setAttributeNS(null, "y", this.y);
    }

    remove() {
	let e = document.getElementById("pkt_" + this.id);
	e.remove();
    }
}

function svg_elem(name, args, content=null) {
    let e = document.createElementNS(svgns, name);
    for (k in args) {
	e.setAttributeNS(null, k, args[k]);
    }
    if (content != null) {
	e.appendChild(content);
    }
    document.getElementById("svg_area").appendChild(e);
}

function draw_pkt(pos, ctx) {
    ctx.fillStyle = "#999900";
    ctx.fillRect(pos[0], pos[1], pkt_height, 2 * pkt_height)
}

function draw_graph() {
    svg_elem("line", {
	"x1": graph_0[0],
	"y1": graph_0[1],
	"x2": graph_0[0] + graph_size[0],
	"y2": graph_0[1],
	"style": "stroke:rgb(0,0,0);stroke-width:2"
    })
    svg_elem("line", {
	"x1": graph_0[0],
	"y1": graph_0[1],
	"x2": graph_0[0],
	"y2": graph_0[1] - graph_size[1],
	"style": "stroke:rgb(0,0,0);stroke-width:2"
    })

    // y axis numbers
    for (let i = 0; i <= 4; i += 1) {
	svg_elem("text",
		 {
		     "x": graph_0[0] - 25,
		     "y": graph_0[1] - graph_size[1] * i / 4.5,
		     "style": "stroke:rgb(0,0,0);stroke-width:1"
		 },
		 document.createTextNode(i * bdp));
    }

    svg_elem("text",
	     {
		 "x": graph_0[0] + graph_size[0] / 2 - 20,
		 "y": graph_0[1] + 20,
		 "style": "stroke:rgb(0,0,0);stroke-width:1"
	     },
	     document.createTextNode("Time"));
    const x1 = graph_0[0] - 30;
    const y1 = graph_0[1] - graph_size[1] / 2 + 20;
    svg_elem("text",
	     {
		 "x": x1,
		 "y": y1,
		 "style": "stroke:rgb(0,0,0);stroke-width:1",
		 "transform": "rotate(-90 " + x1 + " " + y1 + ")"
	     },
	     document.createTextNode("Bytes"));

    // The legend
    svg_elem("text",
	     {
		 "x": graph_0[0] + 50,
		 "y": graph_0[1] - 50,
		 "style": "stroke:rgb(0,0,0);stroke-width:1"
	     },
	     document.createTextNode("Cwnd"));
    svg_elem("text",
	     {
		 "x": graph_0[0] + 50,
		 "y": graph_0[1] - 20,
		 "style": "stroke:rgb(0,0,0);stroke-width:1"
	     },
	     document.createTextNode("Inflight"));
    svg_elem("line", {
	"x1": graph_0[0] + 10,
	"y1": graph_0[1] - 55,
	"x2": graph_0[0] + 40,
	"y2": graph_0[1] - 55,
	"style": "stroke:rgb(128,0,128);stroke-width:2"
    });
    svg_elem("line", {
	"x1": graph_0[0] + 10,
	"y1": graph_0[1] - 25,
	"x2": graph_0[0] + 40,
	"y2": graph_0[1] - 25,
	"style": "stroke:rgb(0,128,128);stroke-width:2"
    });

}

let prev_t = 0;
let prev_cwnd = cur_cwnd;
let prev_inflight = cur_inflight;
function continue_graph() {
    // Plot the current cwnd and inflight onto the graph

    function graph_t(t) {
	// Time is measured in ms and cwnd in packets
	return graph_0[0] + graph_size[0] * t / (max_time * link_intersend);
    }
    function graph_b(b) {
	// Time is measured in ms and cwnd in packets
	return graph_0[1] - graph_size[1] * b / (4.5 * bdp);
    }

    svg_elem("line",
	     {
		 "x1": graph_t(prev_t),
		 "y1": graph_b(prev_cwnd),
		 "x2": graph_t(cur_time),
		 "y2": graph_b(cur_cwnd),
		 "style": "stroke:rgb(128,0,128);stroke-width:1"
	     });
    svg_elem("line",
	     {
		 "x1": graph_t(prev_t),
		 "y1": graph_b(prev_inflight) - 1,
		 "x2": graph_t(cur_time),
		 "y2": graph_b(cur_inflight) - 1,
		 "style": "stroke:rgb(0,128,128);stroke-width:1"
	     });
    prev_t = cur_time;
    prev_cwnd = cur_cwnd;
    prev_inflight = cur_inflight;
}

// All the packets that are being sent
let flying = [];
// All the packets in the buffer
let buffs = [];
// All packets that are currently being dropped
let dropping = [];
// All packets that are returning to sender
let returning = [];

$(document).ready(function() {
    // Create the packets in the buffer
    for (let i = 0; i < 2 * bdp; i += 1) {
	buffs.push(new Packet(buf_end - i * pkt_width, snd_y));
    }
    const buf_start = buf_end - pkt_width * bdp * 2;

    // Create packets coming in from the sender
    for (t in pkt_times) {
	const x = buf_start - pkt_times[t] * link_intersend * vel / frame_interval;
	flying.push(new Packet(x, snd_y));
    }

    draw_graph();

    // Create the buffer
    const e1 = document.createElementNS(svgns, "rect");
    e1.setAttributeNS(null, "width", pkt_width * bdp * 2);
    e1.setAttributeNS(null, "height", 2 * pkt_width + 6);
    e1.setAttributeNS(null, "x", buf_end - (2 * bdp - 1) * pkt_width);
    e1.setAttributeNS(null, "y", snd_y - 3);
    e1.setAttributeNS(null, "style", "fill:none;stroke-width:1;stroke:rgb(0,0,0)");

    // Create the link
    const e2 = document.createElementNS(svgns, "circle");
    e2.setAttributeNS(null, "r", 2 * pkt_width);
    e2.setAttributeNS(null, "cx", buf_end + 3 * pkt_width);
    e2.setAttributeNS(null, "cy", snd_y + pkt_width);
    e2.setAttributeNS(null, "style", "fill:none;stroke-width:1;stroke:rgb(0,0,0)");
    svg_elem("text",
	     {
		 "x": buf_end + 12,
		 "y": snd_y + 15,
		 "style": "stroke-width:1;stroke:rgb(0,0,0)"
	     },
	     document.createTextNode("Link")
	    );

    // Create the sender
    svg_elem("rect",
	     {
		 "x": snd_x - 100,
		 "y": snd_y - 15,
		 "width": 100,
		 "height": 200,
		 "rx": 5,
		 "ry": 5,
		 "style": "fill:none;stroke-width:1;stroke:rgb(0,0,0)"
	     });
    svg_elem("text",
	     {
		 "x": snd_x - 85,
		 "y": 150,
		 "style": "stroke-width:1;stroke:rgb(0,0,0)"
	     },
	     document.createTextNode("Sender")
	    );

    const svg = document.getElementById("svg_area");
    svg.appendChild(e1);
    svg.appendChild(e2);

    // flying.push(new Packet(0, snd_y));
});

setInterval(function () {
    if (paused) {
	return;
    }
    if (stopped) {
	return;
    }
    // for (i in pause_times) {
    // 	if (cur_time == pause_times[i] * link_intersend) {
    // 	    paused = true;
    // 	}
    // }

    // Dequeue packets
    if (cur_time % link_intersend == 0 && buffs.length > 0 && cur_time != 0) {
	returning.push(buffs[0]);
	buffs.splice(0, 1);
    }

    // Fly sent packets forward
    for (i in flying) {
	flying[i].x += vel;
	if (flying[i].x >= buf_start) {
	    if (flying[i].id == 2 * bdp + 1 || flying[i].id == bdp * 4 - 1 || flying[i].id == bdp * 5 - 1) {
		paused = true;
	    }
	    if (flying[i].id == bdp * 6) {
		stopped = true;
	    }

	    // Check if this packet is to be dropped
	    if (buffs.length == 2 * bdp) {
		dropping.push(flying[i]);
		flying.splice(i, 1);
	    }
	    // Put it in the buffer
	    else {
		let end = buf_end;
		if (buffs.length > 0) {
		    end = buffs[0].x;
		}
		flying[i].x = end - buffs.length * pkt_width;
		buffs.push(flying[i]);
		flying.splice(i, 1);
	    }
	}
    }

    // Move packets in buffer forward
    if (buffs.length > 0 && buffs[0].x < buf_end) {
	// Move faster in buffer than in air
	const delta = Math.min(vel / 5, buf_end - buffs[0].x);
	for (i in buffs) {
	    buffs[i].x += delta;
	}
    }

    // Drop packets
    for (i in dropping) {
	if (dropping[i].y < height / 2) {
	    dropping[i].y += vel;
	}
	else {
	    dropping[i].remove()
	    dropping.splice(i, 1);
	}
    }

    // Fly returning packets back
    for (i in returning) {
	if (returning[i].y < return_y) {
	    returning[i].y = Math.min(returning[i].y + vel, return_y);
	}
	else {
	    if (returning[i].x > snd_x) {
		// Hold up the last-bdp packet for a while
		if (returning[i].x < buf_end - pkt_width * 16) {
		    if (returning[i].id == 5 * bdp) {
			// Wait until the last packet is in
			const last = returning[returning.length-1];
			if (last.id < 6 * bdp-1 || last.x > returning[i].x + (bdp-1) * pkt_width) {
			    continue;
			}
			if (last.x > buf_end - pkt_width * 16 + (bdp-1) * pkt_width - vel) {
			    paused = true;
			}
		    }
		}

		returning[i].x -= vel;
		// See if we are held up by a packet in front
		if (i > 0 && returning[i].x <= returning[i-1].x + pkt_width) {
		    returning[i].x = returning[i-1].x + pkt_width
		}
	    }
	    else {
		// Packet returned

		// Update cwnd and inflight
		if (returning[i].id == 2 * bdp + 2) {
		    paused = true;
		}
		if (returning[i].id == 2 * bdp + 3) {
		    cur_cwnd = 2 * bdp;
		    cur_inflight -= 4;
		    paused = true;
		}
		if (returning[i].id > 2 * bdp + 3) {
		    cur_inflight -= 1;
		}

		if (returning[i].id == 5 * bdp + 1) {
		    paused = true;
		}
		if (returning[i].id == 5 * bdp + 2) {
		    cur_inflight -= 8;
		    paused = true
		}

		if (cur_inflight == 0) {
		    paused = true;
		}

		// Remove the packet drawing
		returning[i].remove()
		returning.splice(i, 1);
	    }
	}
    }

    arrs = [flying, buffs, dropping, returning];
    for (i in arrs) {
	for (pkt in arrs[i]) {
	    arrs[i][pkt].redraw();
	}
    }
    continue_graph();

    cur_time += frame_interval;
}, frame_interval);

$(document).on('keypress', function(event) {
    paused = false;
    if (cur_inflight == 0) {
	cur_inflight = 2 * bdp;
	// Transmit that many packets
	for (let i = 0; i < 16; i += 1) {
	    flying.push(new Packet(snd_x - i * pkt_width, snd_y));
	}
    }
});
