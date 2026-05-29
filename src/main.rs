mod phase4;
mod phase5;
mod sparse_engine;
mod synthesizer;

use clap::Parser;
use synthesizer::OutputFormat;

#[derive(Parser)]
#[command(name = "hwc")]
#[command(author = "Hardware Script Team")]
#[command(version = "0.1.0")]
#[command(about = "Hardware Script Compiler - Synthesize hardware designs to manufacturing formats", long_about = None)]
struct Cli {
    /// Input .hw file to compile
    #[arg(value_name = "FILE")]
    input: Option<String>,

    /// Output directory for generated files
    #[arg(short, long, default_value = "build")]
    output: String,

    /// Export to Gerber format (.gtl) for PCB manufacturing
    #[arg(long)]
    gerber: bool,

    /// Export to OBJ format (.obj) for 3D visualization
    #[arg(long)]
    obj: bool,

    /// Export to Blender Python script (.py)
    #[arg(long)]
    blender: bool,

    /// Export to all formats (default if no format specified)
    #[arg(long)]
    all: bool,

    /// Run demo mode (shows all compiler phases)
    #[arg(long)]
    demo: bool,
}

fn main() {
    let cli = Cli::parse();

    // Demo mode
    if cli.demo || cli.input.is_none() {
        run_demo_mode();
        return;
    }

    // Synthesizer mode
    let input_file = cli.input.unwrap();

    // Determine output formats
    let mut formats = Vec::new();
    
    if cli.all || (!cli.gerber && !cli.obj && !cli.blender) {
        // Default: export all formats
        formats.push(OutputFormat::Gerber);
        formats.push(OutputFormat::OBJ);
        formats.push(OutputFormat::Blender);
    } else {
        if cli.gerber {
            formats.push(OutputFormat::Gerber);
        }
        if cli.obj {
            formats.push(OutputFormat::OBJ);
        }
        if cli.blender {
            formats.push(OutputFormat::Blender);
        }
    }

    // Run synthesizer
    match synthesizer::run_synthesizer(&input_file, &cli.output, &formats) {
        Ok(_) => {}
        Err(e) => {
            eprintln!("\n❌ Synthesis failed: {}", e);
            std::process::exit(1);
        }
    }
}

fn run_demo_mode() {
    println!("==================================================");
    println!("🔥 HARDWARE SCRIPT COMPILER (Demo Mode)");
    println!("==================================================\n");
    
    println!("💡 Usage:");
    println!("   hwc <file.hw>                    # Compile and export all formats");
    println!("   hwc <file.hw> --obj              # Export only OBJ");
    println!("   hwc <file.hw> --gerber           # Export only Gerber");
    println!("   hwc <file.hw> --blender          # Export only Blender");
    println!("   hwc <file.hw> --obj --gerber     # Export OBJ and Gerber");
    println!("   hwc <file.hw> -o output_dir      # Specify output directory");
    println!("   hwc --demo                       # Show this demo\n");
    
    println!("Examples:");
    println!("   hwc src/test_board.hw");
    println!("   hwc my_design.hw --obj -o exports");
    println!("   hwc pcb.hw --gerber --blender\n");
    
    println!("{}", "=".repeat(50));
    println!("\nRunning component demos...\n");
    
    // Demonstrate sparse voxel engine
    sparse_engine::run_sparse_demo();
    println!("\n");
    
    // Phase 4: Physics engine
    phase4::run_phase4_demo();
    println!("\n");
    
    // Phase 5: Parser
    phase5::run_phase5_demo();
    
    println!("\n{}", "=".repeat(50));
    println!("\n💡 To compile a real .hw file, run:");
    println!("   hwc src/test_board.hw\n");
}
