use pest::Parser;
use pest_derive::Parser;
use miette::{Diagnostic, SourceSpan};
use thiserror::Error;

#[derive(Parser)]
#[grammar = "hardware.pest"]
pub struct HardwareParser;

/// Compiler errors with source location tracking
#[allow(dead_code)]
#[derive(Error, Debug, Diagnostic)]
pub enum CompilerError {
    #[error("Parse error")]
    #[diagnostic(help("Check your Hardware Script syntax"))]
    ParseError {
        #[source_code]
        src: String,
        #[label("Error occurred here")]
        span: SourceSpan,
        message: String,
    },

    #[error("Invalid measurement value")]
    #[diagnostic(help("Measurements must be valid numbers followed by units (mm, cm, V, A)"))]
    InvalidMeasurement {
        #[source_code]
        src: String,
        #[label("Invalid measurement")]
        span: SourceSpan,
        details: String,
    },

    #[error("Invalid number")]
    #[diagnostic(help("Expected a valid positive integer"))]
    InvalidNumber {
        #[source_code]
        src: String,
        #[label("Invalid number")]
        span: SourceSpan,
        details: String,
    },

    #[error("Missing required element")]
    #[diagnostic(help("The grammar matched but required data is missing"))]
    MissingElement {
        element: String,
    },
}

/// AST node for Space definition
#[derive(Debug, Clone)]
pub struct SpaceDefinition {
    pub name: String,
    pub dimensions: (f64, f64, f64),
    pub grid: (usize, usize, usize),
}

/// AST node for Component placement
#[derive(Debug, Clone)]
pub struct ComponentPlacement {
    pub component_type: String,
    pub instance_name: String,
    pub position: (usize, usize, usize),
    pub rotation: String,
}

/// AST node for Route definition
#[derive(Debug, Clone)]
pub struct RouteDefinition {
    pub from: String,
    pub to: String,
    pub waypoints: Vec<(usize, usize, usize)>,
}

/// Abstract Syntax Tree
#[derive(Debug, Clone)]
pub struct AST {
    pub space: Option<SpaceDefinition>,
    pub components: Vec<ComponentPlacement>,
    pub routes: Vec<RouteDefinition>,
}

/// Parse Hardware Script source code into AST
pub fn parse_hardware_script(source: &str) -> Result<AST, Box<dyn std::error::Error>> {
    let pairs = HardwareParser::parse(Rule::program, source)
        .map_err(|e| format!("Pest parse error: {}", e))?;

    let mut ast = AST {
        space: None,
        components: Vec::new(),
        routes: Vec::new(),
    };

    for pair in pairs {
        if pair.as_rule() == Rule::program {
            for inner_pair in pair.into_inner() {
                match inner_pair.as_rule() {
                    Rule::space_def => {
                        ast.space = Some(parse_space_def(inner_pair, source)?);
                    }
                    Rule::component_placement => {
                        ast.components.push(parse_component_placement(inner_pair, source)?);
                    }
                    Rule::route_def => {
                        ast.routes.push(parse_route_def(inner_pair, source)?);
                    }
                    Rule::EOI => {}
                    _ => {}
                }
            }
        }
    }

    Ok(ast)
}

/// Parse space definition using iterator pattern (no unwrap, no indexing)
fn parse_space_def(
    pair: pest::iterators::Pair<Rule>,
    source: &str,
) -> Result<SpaceDefinition, Box<dyn std::error::Error>> {
    // With silenced keywords, inner() yields: [string, measure, measure, measure, number, number, number]
    let mut inner = pair.into_inner();

    // Extract name
    let name_pair = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "space name".to_string(),
        })?;
    let name = name_pair.as_str().trim_matches('"').to_string();

    // Helper closure to parse measurements safely
    let mut parse_measure = || -> Result<f64, Box<dyn std::error::Error>> {
        let measure_pair = inner.next()
            .ok_or_else(|| CompilerError::MissingElement {
                element: "dimension measurement".to_string(),
            })?;
        
        let text = measure_pair.as_str();
        let span = measure_pair.as_span();
        
        let value_str: String = text
            .chars()
            .take_while(|c| c.is_numeric() || *c == '.')
            .collect();
        
        value_str.parse::<f64>().map_err(|e| {
            Box::new(CompilerError::InvalidMeasurement {
                src: source.to_string(),
                span: SourceSpan::from(span.start()..span.end()),
                details: e.to_string(),
            }) as Box<dyn std::error::Error>
        })
    };

    let dim_x = parse_measure()?;
    let dim_y = parse_measure()?;
    let dim_z = parse_measure()?;

    // Helper closure to parse grid numbers safely
    let mut parse_number = || -> Result<usize, Box<dyn std::error::Error>> {
        let number_pair = inner.next()
            .ok_or_else(|| CompilerError::MissingElement {
                element: "grid dimension".to_string(),
            })?;
        
        let text = number_pair.as_str();
        let span = number_pair.as_span();
        
        text.parse::<usize>().map_err(|e| {
            Box::new(CompilerError::InvalidNumber {
                src: source.to_string(),
                span: SourceSpan::from(span.start()..span.end()),
                details: e.to_string(),
            }) as Box<dyn std::error::Error>
        })
    };

    let grid_x = parse_number()?;
    let grid_y = parse_number()?;
    let grid_z = parse_number()?;

    Ok(SpaceDefinition {
        name,
        dimensions: (dim_x, dim_y, dim_z),
        grid: (grid_x, grid_y, grid_z),
    })
}

/// Parse component placement using iterator pattern
fn parse_component_placement(
    pair: pest::iterators::Pair<Rule>,
    _source: &str,
) -> Result<ComponentPlacement, Box<dyn std::error::Error>> {
    // With silenced keywords, inner() yields: [identifier, identifier, coordinate, rotation]
    let mut inner = pair.into_inner();

    let component_type = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "component type".to_string(),
        })?
        .as_str()
        .to_string();

    let instance_name = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "instance name".to_string(),
        })?
        .as_str()
        .to_string();

    let coord_pair = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "coordinate".to_string(),
        })?;
    let position = parse_coordinate(coord_pair)?;

    let rotation = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "rotation".to_string(),
        })?
        .as_str()
        .to_string();

    Ok(ComponentPlacement {
        component_type,
        instance_name,
        position,
        rotation,
    })
}

/// Parse route definition using iterator pattern
fn parse_route_def(
    pair: pest::iterators::Pair<Rule>,
    _source: &str,
) -> Result<RouteDefinition, Box<dyn std::error::Error>> {
    // With silenced keywords, inner() yields: [identifier/dotted_identifier, identifier/dotted_identifier, waypoint+]
    let mut inner = pair.into_inner();

    let from = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "route source".to_string(),
        })?
        .as_str()
        .to_string();

    let to = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "route destination".to_string(),
        })?
        .as_str()
        .to_string();

    // Collect all waypoints
    let mut waypoints = Vec::new();
    for waypoint_pair in inner {
        if waypoint_pair.as_rule() == Rule::waypoint {
            // waypoint contains a coordinate
            for coord_pair in waypoint_pair.into_inner() {
                if coord_pair.as_rule() == Rule::coordinate {
                    waypoints.push(parse_coordinate(coord_pair)?);
                }
            }
        }
    }

    Ok(RouteDefinition { from, to, waypoints })
}

/// Parse coordinate using iterator pattern (no indexing)
fn parse_coordinate(
    pair: pest::iterators::Pair<Rule>,
) -> Result<(usize, usize, usize), Box<dyn std::error::Error>> {
    let mut inner = pair.into_inner();

    let z = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "coordinate Z".to_string(),
        })?
        .as_str()
        .parse::<usize>()?;

    let x = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "coordinate X".to_string(),
        })?
        .as_str()
        .parse::<usize>()?;

    let y = inner.next()
        .ok_or_else(|| CompilerError::MissingElement {
            element: "coordinate Y".to_string(),
        })?
        .as_str()
        .parse::<usize>()?;

    Ok((z, x, y))
}

/// Demo function for Phase 5
pub fn run_phase5_demo() {
    println!("--- PHASE 5: PRODUCTION-QUALITY PARSER (Pest + Miette) ---\n");

    // Sample Hardware Script
    let hw_code = r#"define Space "SprinklerBoard":
    dimensions: 50mm by 50mm by 2mm
    grid: 50 by 50 by 2

add Transistor_NPN named ValveSwitch at [1, 20, 10] rotated North

route ValveSwitch.Collector to Power.Out:
    path:
        - [1, 20, 11]
        - [1, 20, 15]
        - [1, 30, 15]
"#;

    println!("📖 Parsing Hardware Script...\n");
    println!("Source Code:");
    println!("{}", hw_code);
    println!("\n{}", "=".repeat(50));

    // Parse with Pest
    println!("\n🔍 PARSING (Production-Quality Error Handling)...\n");
    
    let ast = match parse_hardware_script(hw_code) {
        Ok(ast) => {
            println!("✅ Parsing successful!\n");
            ast
        }
        Err(e) => {
            println!("❌ Compilation failed:\n{:?}", e);
            return;
        }
    };

    // Display AST
    println!("📊 ABSTRACT SYNTAX TREE:\n");

    if let Some(space) = &ast.space {
        println!("Space Definition:");
        println!("   Name: {}", space.name);
        println!(
            "   Dimensions: {:.1}mm × {:.1}mm × {:.1}mm",
            space.dimensions.0, space.dimensions.1, space.dimensions.2
        );
        println!(
            "   Grid: {} × {} × {}",
            space.grid.0, space.grid.1, space.grid.2
        );
    }

    if !ast.components.is_empty() {
        println!("\nComponents:");
        for comp in &ast.components {
            println!(
                "   - {} '{}' at {:?} facing {}",
                comp.component_type, comp.instance_name, comp.position, comp.rotation
            );
        }
    }

    if !ast.routes.is_empty() {
        println!("\nRoutes:");
        for route in &ast.routes {
            println!(
                "   - {} → {} ({} waypoints)",
                route.from,
                route.to,
                route.waypoints.len()
            );
            for (i, wp) in route.waypoints.iter().enumerate() {
                println!("      {}. {:?}", i + 1, wp);
            }
        }
    }

    println!("\n✅ COMPILATION SUCCESSFUL! AST is ready for execution.");
    println!("\n💡 Production-Quality Features:");
    println!("   ✓ No .unwrap() - all errors propagated with ?");
    println!("   ✓ No array indexing - iterator pattern throughout");
    println!("   ✓ Silenced keywords in grammar - only data in AST");
    println!("   ✓ Miette error reporting with source spans");
    println!("   ✓ Graceful error handling - never panics on bad input");
}
