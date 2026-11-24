import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#6b7280'))
        self.setStrokeColor(colors.HexColor('#d1d5db'))
        self.setLineWidth(0.5)
        self.line(40, 35, 555, 35)
        self.drawString(40, 24, 'K. J. Somaiya College of Engineering | DevOps LAB CA')
        self.drawRightString(555, 24, f'Page {self._pageNumber}')
        self.restoreState()

def create_report():
    pdf_filename = "DevOps_LABCA_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    PRIMARY = colors.HexColor('#137333') # Somaiya green
    DARK = colors.HexColor('#1f2937')
    MUTED = colors.HexColor('#4b5563')
    BORDER = colors.HexColor('#d1d5db')
    BG_LIGHT = colors.HexColor('#f9fafb')
    HEADER_BG = colors.HexColor('#e6f4ea')

    title_inst = ParagraphStyle(
        'TitleInst',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.black
    )
    title_sub = ParagraphStyle(
        'TitleSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        alignment=1,
        textColor=MUTED
    )
    title_dept = ParagraphStyle(
        'TitleDept',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.black
    )
    title_rec = ParagraphStyle(
        'TitleRec',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=colors.black
    )
    title_main = ParagraphStyle(
        'TitleMain',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=18,
        alignment=1,
        textColor=colors.black
    )
    h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceAfter=6
    )
    h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=DARK,
        spaceBefore=6,
        spaceAfter=3
    )
    body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK,
        spaceAfter=4
    )
    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body,
        fontName='Helvetica-Bold'
    )
    bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )
    caption = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        alignment=1,
        textColor=MUTED,
        spaceBefore=3,
        spaceAfter=6
    )
    code_text = ParagraphStyle(
        'Code_Text',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=DARK
    )
    th_style = ParagraphStyle(
        'TH_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=PRIMARY
    )
    td_style = ParagraphStyle(
        'TD_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=DARK
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("K. J. SOMAIYA COLLEGE OF ENGINEERING", title_inst))
    story.append(Spacer(1, 4))
    story.append(Paragraph("(A constituent college of Somaiya Vidyavihar University)", title_sub))
    story.append(Spacer(1, 30))
    story.append(Paragraph("DEPARTMENT OF INFORMATION TECHNOLOGY", title_dept))
    story.append(Spacer(1, 40))
    story.append(Paragraph("PRACTICAL / EXPERIMENT RECORD", title_rec))
    story.append(Spacer(1, 6))
    story.append(Paragraph("SUBJECT: DEVOPS", title_rec))
    story.append(Spacer(1, 6))
    story.append(Paragraph("DEVOPS LAB CA", title_rec))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Monitoring a Three-Layer Microservices Application<br/>with Docker, Redis, Prometheus and Grafana", title_main))
    story.append(Spacer(1, 40))

    # Student metadata table (NO BATCH)
    student_table_data = [
        [Paragraph("Subject", th_style), Paragraph("DevOps", td_style)],
        [
            Paragraph("Roll numbers & Names", th_style),
            Paragraph("Diya Chugh (16010423033)<br/>Krrish Shah (16010423049)<br/>Prince Parmar (16010423069)", td_style)
        ],
        [Paragraph("Academic year", th_style), Paragraph("2026–2027", td_style)]
    ]
    st_table = Table(student_table_data, colWidths=[140, 360])
    st_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (0,-1), BG_LIGHT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(st_table)

    story.append(Spacer(1, 60))
    story.append(Paragraph("Somaiya Vidyavihar University", title_dept))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXPERIMENT RECORD AND AIM
    # =========================================================================
    story.append(Paragraph("Experiment Record and Aim", h1))
    
    rec_table_data = [
        [Paragraph("Record field", th_style), Paragraph("Value", th_style)],
        [Paragraph("Subject", td_style), Paragraph("DevOps", td_style)],
        [Paragraph("Roll numbers & Names", td_style), Paragraph("Diya Chugh (16010423033) / Krrish Shah (16010423049) / Prince Parmar (16010423069)", td_style)],
        [Paragraph("Assignment", td_style), Paragraph("DevOps LAB CA", td_style)]
    ]
    rt = Table(rec_table_data, colWidths=[140, 375])
    rt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(rt)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Aim", h2))
    story.append(Paragraph(
        "To deploy and monitor the HeatAware AI Climate Intelligence and localized heatwave advisory application "
        "as a Docker Compose microservices system, utilize Redis Streams for asynchronous background notification processing, "
        "collect live metrics with Prometheus at five-second scrape intervals, and visualize end-to-end service health, "
        "queue activity, and compute decisions in a provisioned Grafana observability dashboard.", body
    ))

    story.append(Paragraph("Problem definition", h2))
    story.append(Paragraph(
        "A multi-service application runs across separate processes and isolated containers. Without a consistent startup method "
        "and centralized observability, it is difficult to confirm which services are available, trace a request across service "
        "boundaries, diagnose a stalled queue, or distinguish an idle system from a failed system. This practical brings together "
        "container orchestration, asynchronous messaging, health checks, and metrics dashboards into one cohesive local project.", body
    ))

    story.append(Paragraph("Objectives", h2))
    story.append(Paragraph("• Start the application and observability stack with Docker Compose.", bullet))
    story.append(Paragraph("• Route website API calls through an API Gateway to dedicated backend microservices.", bullet))
    story.append(Paragraph("• Use a Redis Stream and consumer group to decouple emergency advisory calculation from notification processing.", bullet))
    story.append(Paragraph("• Expose standardized service metrics and scrape six application targets at five-second intervals.", bullet))
    story.append(Paragraph("• Visualize container health, request counts, queue lag, inventory telemetry, and advisory outcomes in Grafana.", bullet))

    story.append(Paragraph("Resources needed", h2))
    story.append(Paragraph(
        "Windows 11 workstation, Docker Desktop (WSL2 engine backend), Docker Compose, Python 3.11/FastAPI runtimes, a modern web browser, "
        "project source code, and network access for weather and LLM integrations. MongoDB is configured for user identity. "
        "Redis, Prometheus, Grafana, and six application domain services run inside isolated Docker containers.", body
    ))

    story.append(Paragraph("Practical observation", h2))
    story.append(Paragraph(
        "At the live verification check, Docker Compose reported nine services running concurrently without failures. "
        "Prometheus reported 6 of 6 application targets in the UP state. Redis reported 41 retained stream entries, "
        "0 pending messages, and 0 waiting queue lag. The observed synthetic telemetry counter recorded 30 source=demo events, "
        "verifying metric propagation from application containers to the visualization dashboard.", body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: THEORY OF THE SYSTEM
    # =========================================================================
    story.append(Paragraph("Theory of the System", h1))

    story.append(Paragraph("Microservices", h2))
    story.append(Paragraph(
        "A microservice is an independently runnable component responsible for a focused capability. Services communicate through "
        "network APIs (REST/JSON) or asynchronous messages. This architecture improves deployment velocity and scaling boundaries, "
        "allowing individual features (such as weather forecasting or translation) to scale independently without redeploying the "
        "entire application codebase. However, it introduces distributed failure modes, requiring robust service discovery and observability.", body
    ))

    story.append(Paragraph("Three-layer request path", h2))
    story.append(Paragraph(
        "The browser constitutes the presentation layer (Tier 1), the API Gateway and specialized domain services implement application "
        "business logic (Tier 2), and backing systems such as MongoDB and Redis provide persistence and messaging queues (Tier 3). "
        "Prometheus and Grafana operate as an overarching observability layer that monitors all three tiers simultaneously.", body
    ))

    story.append(Paragraph("Docker and Compose", h2))
    story.append(Paragraph(
        "A Docker image packages an application together with its runtime dependencies into an immutable artifact. A container is a running "
        "instance of an image. Docker Compose describes a multi-container application in YAML, creates a private bridge network (`ms-net`), "
        "applies dependency health constraints, maps selected ports to the host interface, and mounts named volumes for persistent storage.", body
    ))

    story.append(Paragraph("Observability: Metrics and Logs", h2))
    story.append(Paragraph(
        "Observability comprises metrics, logs, and traces. Metrics are numeric measurements recorded over time (counters, gauges, histograms) "
        "that provide high-level health trends. Logs capture contextual text events useful for root-cause diagnosis. Prometheus pulls numeric "
        "samples from service `/metrics` endpoints, while Docker Desktop provides centralized container runtime logs.", body
    ))

    story.append(Paragraph("Redis Streams", h2))
    story.append(Paragraph(
        "A Redis Stream stores ordered append-only entries with unique IDs. A producer appends a job with `XADD`; a consumer group reads "
        "entries with `XREADGROUP`; and successful execution is confirmed with `XACK`. This architectural decoupling allows the API to return "
        "immediately to the client without blocking on slow SMS or dispatch delivery workers.", body
    ))

    story.append(Paragraph("Prometheus and Grafana", h2))
    story.append(Paragraph(
        "Prometheus stores labeled time-series data and evaluates PromQL queries for aggregation and rate calculation. Grafana queries "
        "Prometheus as an automated datasource and renders stat panels, time-series graphs, and health indicators. A flat graph indicates "
        "that no new events occurred in that window; it does not indicate that the monitoring infrastructure has failed.", body
    ))

    story.append(Paragraph("Metric types", h2))
    story.append(Paragraph("• <b>Counter:</b> Cumulative metric that only increases (e.g., <code>gateway_requests_total</code>). Evaluated with <code>rate()</code> or <code>increase()</code>.", bullet))
    story.append(Paragraph("• <b>Gauge:</b> Value that can rise or fall arbitarily (e.g., <code>notification_queue_lag</code>, <code>notification_stream_length</code>).", bullet))
    story.append(Paragraph("• <b>Histogram:</b> Samples observations into configurable buckets plus count and sum (e.g., <code>advisory_duration_seconds</code>) for latency percentiles.", bullet))
    story.append(Paragraph("• <b>Prometheus up:</b> Binary health metric generated automatically during scrape; 1 indicates success, 0 indicates failure.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ARCHITECTURE AND REQUEST FLOW
    # =========================================================================
    story.append(Paragraph("Architecture and Request Flow", h1))
    story.append(Paragraph(
        "The frontend communicates with the API Gateway at port 8000. The Gateway proxies authentication requests to the Auth service, "
        "and orchestrates climate/heatwave advisories by requesting weather data from Weather, sending inputs to Advisory, and obtaining "
        "localized text from Translation. When emergency notification work is dispatched, the Gateway appends an event to Redis, "
        "and the Notification worker processes it asynchronously.", body
    ))
    story.append(Spacer(1, 6))

    arch_box = [
        [Paragraph(
            "<b>HeatAware AI Microservices Request & Observability Telemetry Flow</b><br/>"
            "<i>Compose Network: ms-net | Lines summarize project calls; Prometheus & Grafana observe application health.</i><br/><br/>"
            "<font face='Courier' size='7'>"
            "+----------------+           +------------------+         +-----------------+\n"
            "| Frontend / Web | ---API---> |  Gateway :8000   | ----+-> |   Auth :8001    |\n"
            "|  (React / Dev) |            | REST entrypoint  |     |   +-----------------+\n"
            "+----------------+            +------------------+     |   +-----------------+\n"
            "                               |       |        |      +-> |  Weather :8002  |\n"
            "                               |       |        |          +-----------------+\n"
            "                               |       |        |          +-----------------+\n"
            "            XADD advisory.created      |        +--------> |  Advisory :8003 |\n"
            "                               |       |                   +-----------------+\n"
            "                               v       |                           |\n"
            "                       +---------------+                           v\n"
            "                       |  Redis :6379  |                  +-----------------+\n"
            "                       | Stream Broker |                  |Translation :8004|\n"
            "                       +---------------+                  +-----------------+\n"
            "                               |\n"
            "                          XREADGROUP\n"
            "                               v\n"
            "                       +--------------------+\n"
            "                       | Notification :8005 | ----> Emits Mock SMS Telemetry\n"
            "                       +--------------------+\n\n"
            " [Observability Layer]\n"
            " Prometheus :9090  ==== Scrapes /metrics from 6 app services (5s interval)\n"
            " Grafana :3000     ==== Queries Prometheus Datasource & Renders Live Dashboard\n"
            "</font>", code_text
        )]
    ]
    at = Table(arch_box, colWidths=[515])
    at.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(at)
    story.append(Paragraph("Figure 1. Microservices system architecture, inter-service REST routing, Redis stream queue, and Prometheus scrape topology.", caption))

    story.append(Paragraph("Synchronous advisory flow", h2))
    story.append(Paragraph("1. Frontend sends an authenticated advisory request to the API Gateway on port 8000.", bullet))
    story.append(Paragraph("2. Gateway obtains real-time meteorological observations from the Weather service on port 8002.", bullet))
    story.append(Paragraph("3. Gateway passes temperature, relative humidity, stakeholder category, and zone parameters to the Advisory engine on port 8003.", bullet))
    story.append(Paragraph("4. Gateway requests localized multi-lingual text explanations from the Translation service on port 8004.", bullet))
    story.append(Paragraph("5. Gateway returns the combined emergency response payload to the client and increments request metrics.", bullet))

    story.append(Paragraph("Asynchronous notification flow", h2))
    story.append(Paragraph("1. Gateway serializes advisory fields and pushes an event to Redis Stream <code>advisory.created</code> via <code>XADD</code>.", bullet))
    story.append(Paragraph("2. Notification worker consumer group reads new stream entries using <code>XREADGROUP</code>.", bullet))
    story.append(Paragraph("3. Worker formats localized alert text, masks phone numbers for data privacy, and emits a structured mock SMS log.", bullet))
    story.append(Paragraph("4. Worker acknowledges completion with <code>XACK</code>; stream length and lag gauges are updated for Prometheus.", bullet))

    story.append(Paragraph("Monitoring flow", h2))
    story.append(Paragraph(
        "Every five seconds, Prometheus polls the <code>/metrics</code> endpoint of Gateway, Auth, Weather, Advisory, Translation, "
        "and Notification. Grafana evaluates PromQL expressions against Prometheus over the internal <code>ms-net</code> bridge network.", body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: REPOSITORY DIRECTORY MAP
    # =========================================================================
    story.append(Paragraph("Repository Directory Map", h1))

    dir_map_data = [
        [Paragraph("Directory / File", th_style), Paragraph("Purpose / Responsibility", th_style)],
        [Paragraph("<code>frontend/</code>", td_style), Paragraph("Web interface: climate dashboards, telemetry visualizers, advisory forms, and API clients calling the Gateway.", td_style)],
        [Paragraph("<code>microservices/docker-compose.yml</code>", td_style), Paragraph("Defines 9 multi-container services, port mappings, internal bridge network (<code>ms-net</code>), dependencies, and restart policies.", td_style)],
        [Paragraph("<code>microservices/gateway/src/</code>", td_style), Paragraph("FastAPI reverse proxy, central API entry point, route dispatching, inventory telemetry endpoints, and Prometheus metrics.", td_style)],
        [Paragraph("<code>microservices/auth/src/</code>", td_style), Paragraph("User registration, JWT token generation, session validation, and database abstraction layer.", td_style)],
        [Paragraph("<code>microservices/weather/src/</code>", td_style), Paragraph("Automated Weather Station (AWS) data retrieval, regional forecast adapter, cache handling, and weather scrape metrics.", td_style)],
        [Paragraph("<code>microservices/advisory/main.py</code>", td_style), Paragraph("FastAPI physiological heat stress calculation, NOAA Heat Index logic, stakeholder guidelines, and advisory duration metrics.", td_style)],
        [Paragraph("<code>microservices/translation/src/</code>", td_style), Paragraph("Multi-lingual emergency message localization (English, Hindi, Marathi) and translation counter metrics.", td_style)],
        [Paragraph("<code>microservices/notification/src/</code>", td_style), Paragraph("Redis Streams background worker, consumer group listener, mock-SMS logging, and queue gauge metric exporter.", td_style)],
        [Paragraph("<code>microservices/monitoring/</code>", td_style), Paragraph("Prometheus scrape job configuration (<code>prometheus.yml</code>) and Grafana automatic datasource/dashboard provisioning files.", td_style)],
        [Paragraph("<code>.github/workflows/</code>", td_style), Paragraph("GitHub Actions CI workflow for automated container image compilation and build verification on push events.", td_style)]
    ]
    dmt = Table(dir_map_data, colWidths=[160, 355])
    dmt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(dmt)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Main configuration files", h2))
    story.append(Paragraph("• <b>microservices/docker-compose.yml:</b> Declares nine service containers, container names, exposed host ports, and the private bridge network <code>ms-net</code>.", bullet))
    story.append(Paragraph("• <b>microservices/monitoring/prometheus.yml:</b> Declares six scrape jobs with a five-second global scrape and evaluation interval.", bullet))
    story.append(Paragraph("• <b>microservices/monitoring/grafana/provisioning/datasources/:</b> Provisions Prometheus as the default Grafana datasource.", bullet))
    story.append(Paragraph("• <b>microservices/monitoring/grafana/provisioning/dashboards/:</b> Loads the live preconfigured operational telemetry dashboard.", bullet))
    story.append(Paragraph("• <b>.github/workflows/docker-build.yml:</b> Defines CI automated builds for custom microservice Docker images.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SERVICE DEFINITIONS AND PORTS
    # =========================================================================
    story.append(Paragraph("Service Definitions and Ports", h1))

    svc_data = [
        [Paragraph("Service", th_style), Paragraph("Role / Definition", th_style), Paragraph("Port / Metrics Exported", th_style)],
        [Paragraph("<b>Gateway</b>", td_style), Paragraph("Public API gateway entry point. Routes requests, handles circuit breaker state, records inventory events.", td_style), Paragraph("<b>8000;</b> <code>gateway_requests_total</code>, <code>inventory_actions_total</code>, <code>circuit_breaker_state</code>", td_style)],
        [Paragraph("<b>Auth</b>", td_style), Paragraph("Authenticates clients, hashes credentials, and issues session tokens.", td_style), Paragraph("<b>8001;</b> <code>auth_registrations_total</code>, <code>auth_logins_total</code>", td_style)],
        [Paragraph("<b>Weather</b>", td_style), Paragraph("Fetches AWS weather telemetry, regional forecasts, and cache hit/miss data.", td_style), Paragraph("<b>8002;</b> <code>weather_fetches_total</code>, <code>weather_fetch_duration_seconds</code>", td_style)],
        [Paragraph("<b>Advisory</b>", td_style), Paragraph("Computes heatwave emergency advisories based on temperature, humidity, and stakeholder type.", td_style), Paragraph("<b>8003;</b> <code>advisory_decisions_total</code>, <code>advisory_duration_seconds</code>", td_style)],
        [Paragraph("<b>Translation</b>", td_style), Paragraph("Translates decision guidelines into regional target languages (English, Hindi, Marathi).", td_style), Paragraph("<b>8004;</b> <code>translations_total{language}</code>", td_style)],
        [Paragraph("<b>Notification</b>", td_style), Paragraph("Consumes Redis stream <code>advisory.created</code>; logs mock-SMS dispatch telemetry.", td_style), Paragraph("<b>8005;</b> <code>notifications_sent_total</code>, <code>notification_stream_length</code>, <code>notification_queue_lag</code>", td_style)],
        [Paragraph("<b>Redis</b>", td_style), Paragraph("In-memory broker for Redis Stream queueing. Runs Redis 7 with AOF persistence.", td_style), Paragraph("<b>6379;</b> Inter-container broker on <code>ms-net</code>", td_style)],
        [Paragraph("<b>Prometheus</b>", td_style), Paragraph("Scrapes <code>/metrics</code> from all six microservices every 5 seconds; evaluates PromQL.", td_style), Paragraph("<b>9090;</b> Web UI and TSDB HTTP API", td_style)],
        [Paragraph("<b>Grafana</b>", td_style), Paragraph("Observability dashboard visualization server connecting to Prometheus.", td_style), Paragraph("<b>3000;</b> Web UI live dashboard", td_style)]
    ]
    st = Table(svc_data, colWidths=[80, 245, 190])
    st.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(st)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Local URLs", h2))
    url_data = [
        [Paragraph("Browser Address", th_style), Paragraph("Purpose / Interface", th_style)],
        [Paragraph("<code>http://localhost:8000</code>", td_style), Paragraph("API Gateway entry point and health probe.", td_style)],
        [Paragraph("<code>http://localhost:8000/docs</code>", td_style), Paragraph("Interactive Swagger / OpenAPI documentation for API endpoints.", td_style)],
        [Paragraph("<code>http://localhost:9090/targets</code>", td_style), Paragraph("Prometheus target health status page displaying 6 active scrape endpoints.", td_style)],
        [Paragraph("<code>http://localhost:3000</code>", td_style), Paragraph("Grafana live operational metrics and service dashboard.", td_style)]
    ]
    ut = Table(url_data, colWidths=[180, 335])
    ut.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ut)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: DOCKER COMPOSE PROCEDURE AND EVIDENCE (FIGURE 2)
    # =========================================================================
    story.append(Paragraph("Docker Compose Procedure and Evidence", h1))

    story.append(Paragraph("Startup procedure", h2))
    story.append(Paragraph("1. Launch Docker Desktop on Windows 11 and verify the WSL2 container engine is responsive.", bullet))
    story.append(Paragraph("2. Navigate from the project root into the <code>microservices</code> directory.", bullet))
    story.append(Paragraph("3. Execute: <code>docker compose up --build -d</code> to build custom service images and launch containers in detached mode.", bullet))
    story.append(Paragraph("4. Inspect container execution status: <code>docker compose ps</code>.", bullet))
    story.append(Paragraph("5. Open the Prometheus target health page (<code>:9090/targets</code>) and Grafana dashboard (<code>:3000</code>) in the browser.", bullet))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Docker images supplied", h2))

    img_p2 = "report_assets/fig2_docker_images.jpg"
    if os.path.exists(img_p2):
        story.append(Image(img_p2, width=515, height=247))
    story.append(Paragraph("Figure 2. Docker Desktop image inventory provided by the student group. Shows 10 local images available (6 custom microservices, Redis, Prometheus, Grafana, and Nginx).", caption))

    story.append(Paragraph("Image inventory verification", h2))
    story.append(Paragraph(
        "As verified in Figure 2, the Docker image inventory contains all 10 required container images: "
        "<code>microservices-gateway</code>, <code>microservices-auth</code>, <code>microservices-weather</code>, "
        "<code>microservices-advisory</code>, <code>microservices-translation</code>, <code>microservices-notification</code>, "
        "along with the backing infrastructure images <code>redis:7-alpine</code>, <code>prom/prometheus:latest</code>, "
        "<code>grafana/grafana:latest</code>, and <code>nginx:1.27-alpine</code>.", body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CONTAINER LOG EVIDENCE (FIGURE 3)
    # =========================================================================
    story.append(Paragraph("Container Log Evidence", h1))
    story.append(Paragraph(
        "Container logs provide verifiable runtime evidence that each microservice successfully bound to its designated TCP port, "
        "connected to dependencies across the internal <code>ms-net</code> bridge network, and responded to periodic health and Prometheus scrape probes.", body
    ))
    story.append(Spacer(1, 4))

    img_p3 = "report_assets/fig3_docker_logs.jpg"
    if os.path.exists(img_p3):
        story.append(Image(img_p3, width=515, height=250))
    story.append(Paragraph("Figure 3. Supplied Docker Desktop combined logs show microservices startup, Redis connection, and periodic Prometheus HTTP 200 /metrics scrape requests.", caption))

    story.append(Paragraph("Analysis of runtime log output", h2))
    story.append(Paragraph(
        "The live log stream captured in Figure 3 confirms: (1) The Gateway, Auth, Weather, Advisory, Translation, and Notification "
        "microservices initialized under Uvicorn ASGI servers; (2) The Notification worker initialized its Redis Stream listener; "
        "(3) Prometheus actively polled each microservice's <code>/metrics</code> endpoint at 5-second intervals, returning HTTP 200 OK "
        "consistently; (4) Grafana successfully registered plugins and datasources upon launch.", body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: COMPOSE STACK SCREENSHOT AND RUNTIME (FIGURE 4)
    # =========================================================================
    story.append(Paragraph("Compose Stack Screenshot and Runtime", h1))
    
    img_p4 = "report_assets/fig4a_compose_containers.jpg"
    if os.path.exists(img_p4):
        story.append(Image(img_p4, width=515, height=250))
    story.append(Paragraph("Figure 4. Supplied Docker Desktop Compose view showing the active microservices container group running with 12 CPUs allocated under WSL2.", caption))

    story.append(Paragraph("Current stack observation", h2))
    stack_obs_data = [
        [Paragraph("Compose Service", th_style), Paragraph("Container Role", th_style), Paragraph("Observed Status in Report", th_style)],
        [Paragraph("gateway", td_style), Paragraph("API entry point / Telemetry router", td_style), Paragraph("Up (healthy) :8000", td_style)],
        [Paragraph("auth", td_style), Paragraph("Identity & Token validation", td_style), Paragraph("Up (healthy) :8001", td_style)],
        [Paragraph("weather", td_style), Paragraph("Automated Weather Station adapter", td_style), Paragraph("Up (healthy) :8002", td_style)],
        [Paragraph("advisory", td_style), Paragraph("Physiological heat stress logic", td_style), Paragraph("Up (healthy) :8003", td_style)],
        [Paragraph("translation", td_style), Paragraph("Regional language localization", td_style), Paragraph("Up (healthy) :8004", td_style)],
        [Paragraph("notification", td_style), Paragraph("Redis Stream consumer worker", td_style), Paragraph("Up (healthy) :8005", td_style)],
        [Paragraph("redis", td_style), Paragraph("Stream storage & message broker", td_style), Paragraph("Up (healthy) :6379", td_style)],
        [Paragraph("prometheus", td_style), Paragraph("Time-series metrics collection", td_style), Paragraph("Up :9090", td_style)],
        [Paragraph("grafana", td_style), Paragraph("Observability dashboard visualization", td_style), Paragraph("Up :3000", td_style)]
    ]
    sot = Table(stack_obs_data, colWidths=[100, 245, 170])
    sot.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(sot)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: PROMETHEUS COLLECTION AND TARGET HEALTH (FIGURE 5)
    # =========================================================================
    story.append(Paragraph("Prometheus Collection and Target Health", h1))
    story.append(Paragraph(
        "Each instrumented microservice exposes a plain-text Prometheus exposition format at <code>/metrics</code>. "
        "The Prometheus server connects to these endpoints over the internal bridge network (<code>ms-net</code>) "
        "and stores scraped samples with labeled dimensions such as job, instance, route, and status.", body
    ))
    story.append(Spacer(1, 4))

    img_p5a = "report_assets/fig5a_prometheus_targets.jpg"
    img_p5b = "report_assets/fig5b_prometheus_targets.jpg"
    if os.path.exists(img_p5a):
        story.append(Image(img_p5a, width=515, height=130))
    if os.path.exists(img_p5b):
        story.append(Spacer(1, 4))
        story.append(Image(img_p5b, width=515, height=130))
    story.append(Paragraph("Figure 5. Prometheus target health interface at localhost:9090/targets verifying 6 of 6 application targets in the UP (1/1) state.", caption))

    story.append(Paragraph("Prometheus target health table", h2))
    tgt_data = [
        [Paragraph("Job Name", th_style), Paragraph("Scrape Target Endpoint", th_style), Paragraph("Scrape Interval", th_style), Paragraph("Latest State", th_style)],
        [Paragraph("advisory", td_style), Paragraph("http://advisory:8003/metrics", td_style), Paragraph("5s", td_style), Paragraph("<b>UP</b>", td_style)],
        [Paragraph("auth", td_style), Paragraph("http://auth:8001/metrics", td_style), Paragraph("5s", td_style), Paragraph("<b>UP</b>", td_style)],
        [Paragraph("gateway", td_style), Paragraph("http://gateway:8000/metrics", td_style), Paragraph("5s", td_style), Paragraph("<b>UP</b>", td_style)],
        [Paragraph("notification", td_style), Paragraph("http://notification:8005/metrics", td_style), Paragraph("5s", td_style), Paragraph("<b>UP</b>", td_style)],
        [Paragraph("translation", td_style), Paragraph("http://translation:8004/metrics", td_style), Paragraph("5s", td_style), Paragraph("<b>UP</b>", td_style)],
        [Paragraph("weather", td_style), Paragraph("http://weather:8002/metrics", td_style), Paragraph("5s", td_style), Paragraph("<b>UP</b>", td_style)]
    ]
    tgtt = Table(tgt_data, colWidths=[100, 205, 100, 110])
    tgtt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tgtt)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: METRIC CATALOG AND MEASUREMENT METHOD
    # =========================================================================
    story.append(Paragraph("Metric Catalog and Measurement Method", h1))

    catalog_data = [
        [Paragraph("Metric Name", th_style), Paragraph("Type / Labels", th_style), Paragraph("What It Measures / Evaluates", th_style)],
        [Paragraph("<code>gateway_requests_total</code>", td_style), Paragraph("Counter; method, route, status", td_style), Paragraph("Total API requests routed through the Gateway. Evaluated using rate() or increase().", td_style)],
        [Paragraph("<code>inventory_actions_total</code>", td_style), Paragraph("Counter; action, category, source", td_style), Paragraph("Inventory modifications. source=demo differentiates synthetic evaluation traffic from user actions.", td_style)],
        [Paragraph("<code>news_generation_requests_total</code>", td_style), Paragraph("Counter; result", td_style), Paragraph("LLM automated climate news advisory generation attempts (success or fallback error).", td_style)],
        [Paragraph("<code>weather_fetches_total</code>", td_style), Paragraph("Counter; status", td_style), Paragraph("Automated Weather Station (AWS) data fetch count across monitored weather zones.", td_style)],
        [Paragraph("<code>weather_fetch_duration_seconds</code>", td_style), Paragraph("Histogram", td_style), Paragraph("Latency observed while contacting meteorological telemetry endpoints.", td_style)],
        [Paragraph("<code>advisory_decisions_total</code>", td_style), Paragraph("Counter; decision", td_style), Paragraph("Cumulative climate emergency advisories categorized by outcome severity.", td_style)],
        [Paragraph("<code>advisory_duration_seconds</code>", td_style), Paragraph("Histogram", td_style), Paragraph("Execution time required to compute heat stress indices and synthesize recommendations.", td_style)],
        [Paragraph("<code>translations_total</code>", td_style), Paragraph("Counter; language", td_style), Paragraph("Translations served grouped by language code (en, hi, mr).", td_style)],
        [Paragraph("<code>notifications_sent_total</code>", td_style), Paragraph("Counter", td_style), Paragraph("Advisory jobs processed and acknowledged by the notification worker.", td_style)],
        [Paragraph("<code>notification_stream_length</code>", td_style), Paragraph("Gauge", td_style), Paragraph("Current retained entries in Redis Stream <code>advisory.created</code>.", td_style)],
        [Paragraph("<code>notification_queue_lag</code>", td_style), Paragraph("Gauge", td_style), Paragraph("Undelivered messages awaiting consumer group pickup.", td_style)],
        [Paragraph("<code>notification_redis_up</code>", td_style), Paragraph("Gauge", td_style), Paragraph("Binary connection health indicator for Redis broker (1=healthy, 0=offline).", td_style)],
        [Paragraph("<code>circuit_breaker_state</code>", td_style), Paragraph("Gauge; service", td_style), Paragraph("Circuit breaker state: 0=closed (healthy), 1=open (fallback), 2=half-open.", td_style)]
    ]
    cat_t = Table(catalog_data, colWidths=[150, 140, 225])
    cat_t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(cat_t)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: OBSERVED APPLICATION TELEMETRY GRAPHS
    # =========================================================================
    story.append(Paragraph("Observed Application Telemetry Graphs", h1))
    story.append(Paragraph(
        "To verify that the metrics pipeline actively records and visualizes live application events, 30 demo-labelled requests "
        "were dispatched through the project endpoint <code>POST /api/metrics/inventory</code> and <code>GET /api/advisory</code>. "
        "These synthetic events advance cumulative counter series, allowing Prometheus and Grafana to demonstrate active operational telemetry.", body
    ))
    story.append(Spacer(1, 8))

    # Prometheus ASCII Graph block
    graph_box = [
        [Paragraph(
            "<b>Prometheus Telemetry Query Execution (localhost:9090)</b><br/>"
            "<i>Query: sum(advisory_decisions_total) vs sum(increase(gateway_requests_total[5m]))</i><br/><br/>"
            "<font face='Courier' size='7'>"
            " Events\n"
            "   30 +-----------------------------------------------------------------------* (30 events)\n"
            "      |                                                                       |\n"
            "   20 |                                                                       |\n"
            "      |                                                                       |\n"
            "   10 |                                                                       |\n"
            "      |                                                                       |\n"
            "    0 +-----------------------------------------------------------------------+\n"
            "     16:20                   16:25                   16:30                  16:35\n"
            "                             Time (UTC / Local IST)\n"
            "</font>", code_text
        )]
    ]
    gt = Table(graph_box, colWidths=[515])
    gt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(gt)
    story.append(Paragraph("Figure 6. Cumulative advisory and gateway event counters recorded during the live practical verification.", caption))

    story.append(Paragraph("How to read these telemetry charts", h2))
    story.append(Paragraph("• <b>X-axis:</b> Represents time in evaluation steps. PromQL rate calculations smooth short-term traffic spikes.", bullet))
    story.append(Paragraph("• <b>Y-axis:</b> Represents the cumulative counter value or gauge state. A step increase indicates processed requests.", bullet))
    story.append(Paragraph("• <b>Flat intervals:</b> Flat segments confirm that services are healthy and idle, rather than failing.", bullet))
    story.append(Paragraph("• <b>Label isolation:</b> The <code>source=demo</code> tag isolates evaluation events from production client traffic.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: REDIS STREAM THEORY AND LIVE QUEUE GRAPHS
    # =========================================================================
    story.append(Paragraph("Redis Stream Theory and Live Queue Graphs", h1))
    story.append(Paragraph(
        "The live queue check verified 41 retained stream entries, 0 waiting messages (zero queue lag), 0 pending messages, "
        "and a Redis connection state of 1. These measurements illustrate the operational difference between total stored stream length, "
        "undelivered lag, and delivered unacknowledged jobs.", body
    ))
    story.append(Spacer(1, 6))

    redis_box = [
        [Paragraph(
            "<b>Redis Stream Message State Architecture</b><br/><br/>"
            "<font face='Courier' size='7.5'>"
            " [API Gateway] ---XADD---> [ Redis Stream: advisory.created ]\n"
            "                                   |\n"
            "              +--------------------+--------------------+\n"
            "              | Total Retained: 41 | Undelivered Lag: 0 |\n"
            "              +--------------------+--------------------+\n"
            "                                   |\n"
            "                              XREADGROUP\n"
            "                                   v\n"
            "                    [ Notification Consumer Group ]\n"
            "                                   |\n"
            "                    +------------------------------+\n"
            "                    | Pending Unacknowledged: 0    |\n"
            "                    | Emits Mock SMS & Calls XACK  |\n"
            "                    +------------------------------+\n"
            "</font>", code_text
        )]
    ]
    rbt = Table(redis_box, colWidths=[515])
    rbt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(rbt)
    story.append(Paragraph("Figure 7. Redis Stream lifecycle: producer XADD, consumer group XREADGROUP, worker mock SMS processing, and XACK confirmation.", caption))

    story.append(Paragraph("Message lifecycle", h2))
    story.append(Paragraph("1. <b>Enqueue:</b> The API Gateway serializes advisory notifications into Redis Stream <code>advisory.created</code> using <code>XADD</code>.", bullet))
    story.append(Paragraph("2. <b>Consume:</b> The notification consumer group reads new entries via <code>XREADGROUP</code>.", bullet))
    story.append(Paragraph("3. <b>Process:</b> The worker masks recipient contact info and writes a structured mock SMS log.", bullet))
    story.append(Paragraph("4. <b>Acknowledge:</b> The worker commits completion with <code>XACK</code>, resetting pending counters.", bullet))

    story.append(Paragraph("Redis persistence and inspection commands", h2))
    story.append(Paragraph("<code>docker compose exec redis redis-cli PING</code> → Verifies broker liveness (PONG).", bullet))
    story.append(Paragraph("<code>docker compose exec redis redis-cli XLEN advisory.created</code> → Returns stream entry count.", bullet))
    story.append(Paragraph("<code>docker compose exec redis redis-cli XINFO GROUPS advisory.created</code> → Checks consumer group lag.", bullet))
    story.append(Paragraph("<code>docker compose exec redis redis-cli XPENDING advisory.created notification-group</code> → Checks unacked jobs.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: GRAFANA DASHBOARD AND PANEL INTERPRETATION (FIGURE 9)
    # =========================================================================
    story.append(Paragraph("Grafana Dashboard and Panel Interpretation", h1))
    story.append(Paragraph(
        "Grafana is provisioned with a Prometheus datasource at <code>http://prometheus:9090</code> and displays the preconfigured "
        "Microservices Live Dashboard. It converts raw PromQL metrics into an intuitive, real-time visualization interface.", body
    ))
    story.append(Spacer(1, 4))

    img_p9 = "report_assets/fig9_grafana_dashboard.jpg"
    if os.path.exists(img_p9):
        story.append(Image(img_p9, width=515, height=250))
    story.append(Paragraph("Figure 8. Supplied live Grafana dashboard showing 6/6 Targets UP, Redis Connected=1, Stream Length=41, Queue Lag=0, and active telemetry graphs.", caption))

    story.append(Paragraph("Panel interpretation table", h2))
    panel_data = [
        [Paragraph("Dashboard Panel", th_style), Paragraph("Underlying Query / Metric", th_style), Paragraph("Operational Interpretation", th_style)],
        [Paragraph("Targets UP", td_style), Paragraph("<code>sum(up)</code>", td_style), Paragraph("Value <b>6</b> confirms all 6 instrumented microservice containers are healthy and scraping.", td_style)],
        [Paragraph("Redis Connected", td_style), Paragraph("<code>notification_redis_up</code>", td_style), Paragraph("Value <b>1</b> confirms active TCP connection between notification worker and Redis broker.", td_style)],
        [Paragraph("Stream Length", td_style), Paragraph("<code>notification_stream_length</code>", td_style), Paragraph("Value <b>41</b> shows retained entries maintained in the persistent Redis stream.", td_style)],
        [Paragraph("Queue Lag", td_style), Paragraph("<code>notification_queue_lag</code>", td_style), Paragraph("Value <b>0</b> verifies that no messages are backlogged or stuck in the queue.", td_style)],
        [Paragraph("Advisories Computed", td_style), Paragraph("<code>sum(advisory_decisions_total)</code>", td_style), Paragraph("Active series confirming 30 emergency advisory computations were recorded.", td_style)]
    ]
    pt = Table(panel_data, colWidths=[120, 165, 230])
    pt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pt)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: WEBSITE FEATURES AND SITE-TO-METRIC FLOW
    # =========================================================================
    story.append(Paragraph("Website Features and Site-to-Metric Flow", h1))
    story.append(Paragraph(
        "The HeatAware AI web platform interfaces directly with the containerized microservices stack. "
        "User actions, meteorological queries, and inventory updates emit structured telemetry to the Gateway, "
        "populating Prometheus metrics.", body
    ))
    story.append(Spacer(1, 6))

    web_data = [
        [Paragraph("Web Portal / Route", th_style), Paragraph("Portal Purpose / Features", th_style), Paragraph("DevOps & Microservices Relationship", th_style)],
        [Paragraph("Overview & Architecture<br/>(<code>index.html</code>)", td_style), Paragraph("System introduction, stakeholder mapping, live clock, 3-layer architecture visualizer.", td_style), Paragraph("Presentation tier (Tier 1); documents system architecture and routes.", td_style)],
        [Paragraph("Forecast Watch<br/>(<code>dashboard.html</code>)", td_style), Paragraph("Regional synoptic weather forecast, heat anomaly metrics, warning severity cards.", td_style), Paragraph("Calls Weather microservice (port 8002) through API Gateway (port 8000).", td_style)],
        [Paragraph("Live AWS Telemetry<br/>(<code>monitoring.html</code>)", td_style), Paragraph("IoT Automated Weather Station telemetry, 5-second polling loop simulation.", td_style), Paragraph("Simulates field telemetry ingestion; correlates with weather service cache metrics.", td_style)],
        [Paragraph("Alerts & Advisories<br/>(<code>advisories.html</code>)", td_style), Paragraph("Dynamic heat advisory generation, stakeholder persona selection, multi-lingual output.", td_style), Paragraph("Triggers Advisory (8003), Translation (8004), and Redis Stream notification jobs.", td_style)],
        [Paragraph("Research Data Portal<br/>(<code>research.html</code>)", td_style), Paragraph("Scientific archives, downloadable sample CSV telemetry datasets, IMD calibration protocols.", td_style), Paragraph("Demonstrates open data accessibility and dataset distribution.", td_style)]
    ]
    wt = Table(web_data, colWidths=[130, 215, 170])
    wt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(wt)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Observed architectural benefits", h2))
    story.append(Paragraph("• <b>Fault Isolation:</b> If the advisory calculation container experiences peak load, weather observation and user authentication continue running unimpeded.", bullet))
    story.append(Paragraph("• <b>Independent Scalability:</b> The stateless Advisory and Translation containers can be scaled horizontally without replicating the database or caching brokers.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: GITHUB ACTIONS AND CONTAINER BUILD FLOW
    # =========================================================================
    story.append(Paragraph("GitHub Actions and Container Build Flow", h1))
    story.append(Paragraph(
        "The project incorporates continuous integration via GitHub Actions configured in <code>.github/workflows/docker-build.yml</code>. "
        "The workflow automates container compilation, catching syntax or dependency errors prior to deployment.", body
    ))
    story.append(Spacer(1, 6))

    ci_box = [
        [Paragraph(
            "<b>Conceptual CI/CD Pipeline Flow</b><br/><br/>"
            "<font face='Courier' size='7.5'>"
            "+----------------+\n"
            "| Developer Push | ----> Git Push to main branch (krrishshah007/Devops-Labca)\n"
            "+----------------+\n"
            "        |\n"
            "        v\n"
            "+----------------+\n"
            "| GitHub Actions | ----> Checks out code, configures Docker Buildx engine\n"
            "+----------------+\n"
            "        |\n"
            "        v\n"
            "+----------------+\n"
            "| Container Build| ----> Concurrently builds 6 custom application service images\n"
            "+----------------+\n"
            "        |\n"
            "        v\n"
            "+----------------+\n"
            "| Validated Test | ----> Verifies Dockerfile context integrity and health probes\n"
            "+----------------+\n"
            "        |\n"
            "        v\n"
            "+----------------+\n"
            "| Registry Ready | ----> Validated images ready for deployment to Amazon ECR / ECS\n"
            "+----------------+\n"
            "</font>", code_text
        )]
    ]
    cbt = Table(ci_box, colWidths=[515])
    cbt.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(cbt)
    story.append(Paragraph("Figure 9. Continuous Integration (CI) container compilation and image verification workflow.", caption))

    story.append(Paragraph("What the workflow demonstrates", h2))
    story.append(Paragraph("• <b>Automated Build Triggers:</b> Pushes and pull requests to <code>main</code> trigger automated multi-stage builds.", bullet))
    story.append(Paragraph("• <b>Early Error Detection:</b> Catches missing Python packages, broken dependencies, or invalid syntax before manual deployment.", bullet))
    story.append(Paragraph("• <b>Immutable Artifacts:</b> Validates container images for repeatable deployment across test and production environments.", bullet))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: PROPOSED AWS DEPLOYMENT VIEW
    # =========================================================================
    story.append(Paragraph("Proposed AWS Deployment View", h1))
    story.append(Paragraph(
        "To translate the local Docker Compose system into an enterprise cloud architecture, each on-premise component "
        "maps to an equivalent Amazon Web Services (AWS) managed service, providing autoscaling, high availability, and operational resilience.", body
    ))
    story.append(Spacer(1, 6))

    aws_data = [
        [Paragraph("Local Component", th_style), Paragraph("Proposed AWS Mapping", th_style), Paragraph("Architectural Purpose in Cloud", th_style)],
        [Paragraph("Custom Docker Images", td_style), Paragraph("Amazon Elastic Container Registry (ECR)", td_style), Paragraph("Secure, private container image registry with vulnerability scanning.", td_style)],
        [Paragraph("Gateway & Domain Services", td_style), Paragraph("Amazon ECS on AWS Fargate", td_style), Paragraph("Serverless container orchestration running services without managing EC2 instances.", td_style)],
        [Paragraph("Public API Entry", td_style), Paragraph("Application Load Balancer (ALB)", td_style), Paragraph("SSL/TLS termination, health checking, and path-based routing to Gateway tasks.", td_style)],
        [Paragraph("Redis Streams Broker", td_style), Paragraph("Amazon ElastiCache for Redis", td_style), Paragraph("Managed, multi-AZ Redis cluster with automated failover and persistence.", td_style)],
        [Paragraph("Prometheus Server", td_style), Paragraph("Amazon Managed Service for Prometheus (AMP)", td_style), Paragraph("Secure, highly available, serverless Prometheus-compatible metrics ingestion.", td_style)],
        [Paragraph("Grafana Dashboards", td_style), Paragraph("Amazon Managed Grafana (AMG)", td_style), Paragraph("Fully managed dashboard visualization integrated with AWS IAM and SSO.", td_style)],
        [Paragraph("User Identity / Auth", td_style), Paragraph("MongoDB Atlas on AWS / Amazon DocumentDB", td_style), Paragraph("Managed NoSQL document database with automated backups and encryption.", td_style)],
        [Paragraph("Environment Secrets", td_style), Paragraph("AWS Secrets Manager / SSM Parameter Store", td_style), Paragraph("Centralized management for API keys and JWT signing secrets.", td_style)],
        [Paragraph("Container Logs", td_style), Paragraph("Amazon CloudWatch Logs", td_style), Paragraph("Centralized aggregation and indexing of container stdout/stderr log streams.", td_style)]
    ]
    at2 = Table(aws_data, colWidths=[120, 175, 220])
    at2.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.75, BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,0), HEADER_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(at2)
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Note:</b> This architectural mapping illustrates the target enterprise production deployment for HeatAware AI; actual verification in this practical was performed using local Docker Compose.", caption))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: RESULTS, KNOWN LIMITATIONS, AND CONCLUSION
    # =========================================================================
    story.append(Paragraph("Results, Known Limitations, and Conclusion", h1))

    story.append(Paragraph("Results", h2))
    story.append(Paragraph("• Docker Compose successfully launched and maintained nine containers in the <code>ms-net</code> bridge network.", bullet))
    story.append(Paragraph("• Prometheus reported all six configured application scrape targets in the <b>UP (1/1)</b> state at 5-second intervals.", bullet))
    story.append(Paragraph("• Redis Stream <code>advisory.created</code> retained 41 entries with 0 queue lag and 0 pending unacknowledged messages.", bullet))
    story.append(Paragraph("• 30 synthetic inventory and advisory events (<code>source=demo</code>) were processed and visualized on the live charts.", bullet))
    story.append(Paragraph("• The preconfigured Grafana dashboard was provisioned automatically and displayed live operational metrics.", bullet))

    story.append(Paragraph("Known limitations", h2))
    story.append(Paragraph("• <b>Mock SMS:</b> The notification worker emits mock SMS logs; no real external cellular SMS gateway was configured.", bullet))
    story.append(Paragraph("• <b>Local Environment:</b> Testing was executed locally using Docker Desktop on Windows 11 with WSL2 rather than on live AWS cloud infrastructure.", bullet))
    story.append(Paragraph("• <b>Synthetic Telemetry:</b> The 30 demo-labelled inventory actions represent synthetic test events used to verify chart responsiveness.", bullet))

    story.append(Paragraph("Conclusion", h2))
    story.append(Paragraph(
        "This practical successfully demonstrates the end-to-end deployment and observability of a three-layer microservices architecture. "
        "By containerizing the HeatAware AI platform into discrete services (Gateway, Auth, Weather, Advisory, Translation, Notification), "
        "the system achieves loose coupling, fault isolation, and independent scalability. Asynchronous messaging via Redis Streams "
        "prevents client request blocking, while the unified Prometheus and Grafana stack provides real-time operational visibility into "
        "container health, request volumes, and queue performance. The live evidence confirms that all services and scrape jobs operated "
        "reliably throughout the evaluation.", body
    ))

    story.append(Paragraph("References", h2))
    story.append(Paragraph("1. GitHub Repository: https://github.com/krrishshah007/Devops-Labca", bullet))
    story.append(Paragraph("2. Docker Compose Configuration: <code>microservices/docker-compose.yml</code>", bullet))
    story.append(Paragraph("3. Prometheus Configuration: <code>microservices/monitoring/prometheus.yml</code>", bullet))
    story.append(Paragraph("4. Grafana Provisioning: <code>microservices/monitoring/grafana/provisioning/</code>", bullet))
    story.append(Paragraph("5. Live Docker Desktop and Prometheus/Grafana runtime observations, November 2026.", bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report generated successfully: {pdf_filename}")

if __name__ == "__main__":
    create_report()
