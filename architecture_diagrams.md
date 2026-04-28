# Day 1 & Day 2 Agent Architecture Diagrams

## Day 1: Automated PHP Docblock Generator

```mermaid
architecture-beta
    group agent_system(Cloud)[Day 1 Agent System]
    
    service agent(server)[ReAct Agent Loop] in agent_system
    service tools(database)[Agent Tools] in agent_system
    
    service llm(cloud)[Gemini API]
    service filesystem(disk)[Local File System]
    
    agent:R --> L:tools
    
    tools:T --> B:llm
    tools:B --> T:filesystem
    
    %% Note: architecture-beta is newer, let's use standard graph TD for better compatibility
```

Let's use a standard `graph TD` for better rendering across tools.

### Day 1 Architecture
```mermaid
graph TD
    subgraph Day 1 Agent System
        A[ReAct Agent Loop]
        T_Read[Tool: read_file]
        T_Gen[Tool: generate_docblock]
        T_Write[Tool: write_file]
        
        A <-->|Observation/Action| T_Read
        A <-->|Observation/Action| T_Gen
        A <-->|Observation/Action| T_Write
    end

    subgraph External Resources
        FS[(Local File System\n'sample_controller.php')]
        LLM((Gemini API\nLLM Service))
    end

    T_Read <--> FS
    T_Write --> FS
    T_Gen <--> LLM
```

---

### Day 2 Architecture
```mermaid
graph TD
    subgraph Day 2 Agent System
        A2[ReAct Agent Loop\n'agent.py']
        Reg[Tool Registry\n'registry.py']
        
        subgraph Tools Implementation
            T_Search[search_products]
            T_Order[get_order_details]
            T_Inv[check_inventory]
            T_Ticket[create_support_ticket]
        end
        
        subgraph Data Validation
            P_Models[[Pydantic Models\n'models.py']]
        end
        
        subgraph Mock Database
            M_Data[(Mock Data\n'mock_data.py')]
        end
        
        A2 -->|Action: tool_name, params| Reg
        Reg -->|Dispatches Call| T_Search
        Reg -->|Dispatches Call| T_Order
        Reg -->|Dispatches Call| T_Inv
        Reg -->|Dispatches Call| T_Ticket
        
        T_Search & T_Order & T_Inv & T_Ticket <-->|Read/Write| M_Data
        
        T_Search & T_Order & T_Inv & T_Ticket -->|Returns Typed Data| P_Models
        P_Models -->|JSON Dump Observation| A2
    end
```
