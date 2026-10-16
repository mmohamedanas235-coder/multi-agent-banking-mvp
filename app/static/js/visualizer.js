/**
 * Multi-Agent Dynamic DAG Visualizer
 * Renders SVG network topology and animates active agents & message vectors in real-time.
 */

class AgentDAGVisualizer {
  constructor(svgId) {
    this.svg = document.getElementById(svgId);
    this.nodes = {
      supervisor: { x: 170, y: 35, label: "Supervisor", icon: "🤖", color: "#38bdf8" },
      customer: { x: 50, y: 95, label: "Customer", icon: "👤", color: "#818cf8" },
      risk: { x: 120, y: 140, label: "Risk/Fraud", icon: "🛡️", color: "#f43f5e" },
      credit: { x: 220, y: 140, label: "Credit/Loan", icon: "💳", color: "#34d399" },
      compliance: { x: 290, y: 95, label: "Compliance", icon: "⚖️", color: "#fbbf24" },
      notification: { x: 170, y: 95, label: "Notification", icon: "🔔", color: "#c084fc" }
    };
    this.activeNodes = new Set();
    this.init();
  }

  init() {
    if (!this.svg) return;
    this.render();
  }

  render() {
    this.svg.innerHTML = "";
    
    // Create links from supervisor to specialists
    const linksGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    linksGroup.setAttribute("class", "dag-links");

    const sup = this.nodes.supervisor;
    Object.keys(this.nodes).forEach(key => {
      if (key === "supervisor") return;
      const target = this.nodes[key];
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", sup.x);
      line.setAttribute("y1", sup.y);
      line.setAttribute("x2", target.x);
      line.setAttribute("y2", target.y);
      line.setAttribute("stroke", this.activeNodes.has(key) ? target.color : "rgba(255,255,255,0.12)");
      line.setAttribute("stroke-width", this.activeNodes.has(key) ? "2.5" : "1");
      if (this.activeNodes.has(key)) {
        line.setAttribute("stroke-dasharray", "4,3");
        line.innerHTML = `<animate attributeName="stroke-dashoffset" values="20;0" dur="0.8s" repeatCount="indefinite" />`;
      }
      linksGroup.appendChild(line);
    });
    this.svg.appendChild(linksGroup);

    // Create Nodes
    const nodesGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    nodesGroup.setAttribute("class", "dag-nodes");

    Object.keys(this.nodes).forEach(key => {
      const n = this.nodes[key];
      const isActive = this.activeNodes.has(key) || (key === "supervisor" && this.activeNodes.size > 0);
      
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("class", `dag-node ${isActive ? "active" : ""}`);
      g.setAttribute("transform", `translate(${n.x}, ${n.y})`);

      // Outer glow circle if active
      if (isActive) {
        const glow = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        glow.setAttribute("r", "20");
        glow.setAttribute("fill", n.color);
        glow.setAttribute("opacity", "0.25");
        glow.innerHTML = `<animate attributeName="r" values="18;23;18" dur="1.5s" repeatCount="indefinite"/>`;
        g.appendChild(glow);
      }

      // Base circle
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("r", "14");
      circle.setAttribute("fill", isActive ? n.color : "#1e293b");
      circle.setAttribute("stroke", isActive ? "#ffffff" : "rgba(255,255,255,0.2)");
      circle.setAttribute("stroke-width", "1.5");
      g.appendChild(circle);

      // Icon / text
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("dy", "4");
      text.setAttribute("font-size", "10");
      text.textContent = n.icon;
      g.appendChild(text);

      // Label below
      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("text-anchor", "middle");
      label.setAttribute("dy", "24");
      label.setAttribute("font-size", "8");
      label.setAttribute("font-family", "Inter, sans-serif");
      label.setAttribute("fill", isActive ? "#f8fafc" : "#94a3b8");
      label.setAttribute("font-weight", isActive ? "600" : "400");
      label.textContent = n.label;
      g.appendChild(label);

      nodesGroup.appendChild(g);
    });

    this.svg.appendChild(nodesGroup);
  }

  highlightAgents(agentList) {
    this.activeNodes.clear();
    agentList.forEach(name => {
      const lower = name.toLowerCase();
      if (lower.includes("supervisor")) this.activeNodes.add("supervisor");
      if (lower.includes("customer")) this.activeNodes.add("customer");
      if (lower.includes("risk") || lower.includes("fraud")) this.activeNodes.add("risk");
      if (lower.includes("credit") || lower.includes("loan")) this.activeNodes.add("credit");
      if (lower.includes("compliance") || lower.includes("aml")) this.activeNodes.add("compliance");
      if (lower.includes("notification")) this.activeNodes.add("notification");
    });
    this.render();
  }

  reset() {
    this.activeNodes.clear();
    this.render();
  }
}
